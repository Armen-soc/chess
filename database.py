import psycopg2
from psycopg2 import sql, OperationalError, IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import re


class ChessDB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="chess_db",
                user="postgres",
                password="King7s04",
                host="localhost"
            )
            self.conn.autocommit = False  # Explicit transactions
            self.cur = self.conn.cursor()
            # self.create_tables()
        except OperationalError as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def create_tables(self):
        """Create tables if they don't exist with proper column sizes"""
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                    color VARCHAR(5) NOT NULL,
                    moves TEXT,
                    won BOOLEAN,
                    game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    opponent_id INTEGER REFERENCES players(id) ON DELETE SET NULL
                )
            """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to create tables: {e}")

    def _validate_credentials(self, username, password):
        """Validate username and password according to requirements"""
        if not username or not password:
            raise ValueError("Username and password are required")

        username = username.strip()
        password = password.strip()

        # Username validation
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(username) > 50:
            raise ValueError("Username must be less than 50 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("Username can only contain letters, numbers and underscores")

        # Password validation
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if len(password) > 100:
            raise ValueError("Password must be less than 100 characters")

        return username, password

    def register_player(self, username, password):

        """Register a new player with proper validation and error handling"""
        try:
            username, password = self._validate_credentials(username, password)

            password_hash = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=16
            )

            if len(password_hash) > 255:
                raise RuntimeError("Password hash too long for storage")

            try:
                self.cur.execute(
                    "INSERT INTO players (username, password_hash) VALUES (%s, %s) RETURNING id",
                    (username, password_hash)
                )
                player_id = self.cur.fetchone()[0]
                
                self.conn.commit()
                return player_id
            except IntegrityError:
                self.conn.rollback()
                raise ValueError("Username already exists")
            except Exception as e:
                self.conn.rollback()
                raise RuntimeError(f"Database error during registration: {str(e)}")

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise RuntimeError(f"Registration error: {str(e)}")

    def authenticate_player(self, username, password):
        """Authenticate a player with debug logging"""
        try:
            username = username.strip()
            print(f"[DEBUG] Authenticating username: '{username}'")

            if not username or not password:
                print("[DEBUG] Missing username or password")
                return None

            self.cur.execute(
                "SELECT id, password_hash FROM players WHERE username = %s",
                (username,)
            )
            result = self.cur.fetchone()

            if result:
                player_id, stored_hash = result
                if check_password_hash(stored_hash, password):
                    print("[DEBUG] Password is correct")
                    self.conn.commit()
                    return player_id
                else:
                    print("[DEBUG] Password is incorrect")
            else:
                print("[DEBUG] Username not found in DB")

            return None
        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Authentication failed: {e}")
            return None


    def save_game(self, player_id, color, moves, won, opponent_id=None):
        """Save game data to database with improved error handling"""
        try:
            if not player_id or not color or not moves:
                return False

            self.cur.execute(
                """INSERT INTO game_history 
                   (player_id, color, moves, won, opponent_id) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (player_id, color[:5], moves, bool(won), opponent_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def close(self):
        """Close database connection safely"""
        try:
            if hasattr(self, 'cur') and self.cur and not self.cur.closed:
                self.cur.close()
            if hasattr(self, 'conn') and self.conn and not self.conn.closed:
                self.conn.close()
        except Exception:
            pass  # Fail silently during close


    def get_username_by_id(self, player_id):
        """Get username by player ID"""
        try:
            self.cur.execute(
                "SELECT username FROM players WHERE id = %s",
                (player_id,)
            )
            result = self.cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error fetching username: {e}")
            return "Unknown"

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()
