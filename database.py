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
            self.create_tables()
        except OperationalError as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def create_tables(self):
        """Create tables if they don't exist"""
        try:
            self.cur.execute("""
                             CREATE TABLE IF NOT EXISTS players
                             (
                                 id
                                 SERIAL
                                 PRIMARY
                                 KEY,
                                 username
                                 VARCHAR
                             (
                                 50
                             ) UNIQUE NOT NULL,
                                 password_hash VARCHAR
                             (
                                 128
                             ) NOT NULL
                                 )
                             """)

            self.cur.execute("""
                             CREATE TABLE IF NOT EXISTS game_history
                             (
                                 id
                                 SERIAL
                                 PRIMARY
                                 KEY,
                                 player_id
                                 INTEGER
                                 REFERENCES
                                 players
                             (
                                 id
                             ),
                                 color VARCHAR
                             (
                                 5
                             ) NOT NULL,
                                 moves TEXT,
                                 won BOOLEAN,
                                 game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                 )
                             """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to create tables: {e}")

    def _validate_password(self, password):
        """Check password meets minimum requirements"""
        if len(password) < 6:  # Reduced from 8 to 6 for better UX
            raise ValueError("Password must be at least 6 characters long")
        # Removed other complexity requirements for simplicity

    def register_player(self, username, password):
        """Register a new player"""
        if not username or not password:
            raise ValueError("Username and password are required")

        try:
            self._validate_password(password)
        except ValueError as e:
            # Return None instead of raising exception to match original behavior
            return None

        password_hash = generate_password_hash(password)

        try:
            self.cur.execute(
                "INSERT INTO players (username, password_hash) VALUES (%s, %s) RETURNING id",
                (username.strip(), password_hash)
            )
            player_id = self.cur.fetchone()[0]
            self.conn.commit()
            return player_id
        except IntegrityError:
            self.conn.rollback()
            return None  # Match original behavior
        except Exception as e:
            self.conn.rollback()
            return None  # Match original behavior

    def authenticate_player(self, username, password):
        """Authenticate a player"""
        if not username or not password:
            return None

        try:
            self.cur.execute(
                "SELECT id, password_hash FROM players WHERE username = %s",
                (username.strip(),)
            )
            result = self.cur.fetchone()
            if result and check_password_hash(result[1], password):
                return result[0]  # Return player ID
            return None
        except Exception as e:
            return None  # Match original behavior

    def save_game(self, player_id, color, moves, won):
        """Save game data to database"""
        if not player_id or not color or not moves:
            return False  # Match original behavior by failing silently

        try:
            self.cur.execute(
                "INSERT INTO game_history (player_id, color, moves, won) VALUES (%s, %s, %s, %s)",
                (player_id, color[:5], moves, bool(won))
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False  # Match original behavior by failing silently

    def close(self):
        """Close database connection"""
        try:
            if hasattr(self, 'cur') and self.cur and not self.cur.closed:
                self.cur.close()
            if hasattr(self, 'conn') and self.conn and not self.conn.closed:
                self.conn.close()
        except Exception:
            pass  # Fail silently during close

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()