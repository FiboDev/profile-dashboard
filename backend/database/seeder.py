import psycopg2
import os
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

load_env()
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://admin:password@localhost:5432/factored_employees") # only dev mode

def seed_database():
    print("🌱 Starting database seeding...")
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    try:
        print("👥 Creating users...")
        
        users = [
            ("Juan Pérez", "Senior Developer", "juan.perez@example.com", "password123", "https://api.dicebear.com/7.x/avataaars/svg?seed=juan"),
            ("María García", "Data Scientist", "maria.garcia@example.com", "password456", "https://api.dicebear.com/7.x/avataaars/svg?seed=maria"),
            ("Carlos López", "DevOps Engineer", "carlos.lopez@example.com", "password789", "https://api.dicebear.com/7.x/avataaars/svg?seed=carlos")
        ]
        
        for name, position, email, password, avatar in users:
            cur.execute("SELECT id FROM \"user\" WHERE email = %s", (email,))
            if cur.fetchone():
                print(f"   ⚠️  User {email} already exists, skipping...")
                continue

            cur.execute("""
                INSERT INTO "user" (name, position, email, password, avatar_url, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """, (name, position, email, password, avatar))
            print(f"   ✅ Created user: {name} ({email})")
        
        conn.commit()
        
        print("🛠️  Creating skills...")
        
        skills = [
            ("Python", "Programming", "Advanced Python programming", 9, 1),
            ("SQL", "Database", "Database design and optimization", 8, 1),
            ("JavaScript", "Programming", "Frontend and backend development", 7, 1),
            ("Docker", "DevOps", "Containerization and deployment", 6, 1),
            ("Machine Learning", "Data Science", "ML algorithms and model deployment", 8, 1),
            ("FastAPI", "Framework", "REST API development", 8, 1),
            
            ("R", "Programming", "Statistical analysis and visualization", 9, 2),
            ("Python", "Programming", "Data analysis and ML", 8, 2),
            ("Apache Spark", "Big Data", "Large-scale data processing", 7, 2),
            ("Tableau", "Visualization", "Data visualization and dashboards", 8, 2),
            ("Statistics", "Data Science", "Statistical modeling and analysis", 9, 2),
            ("SQL", "Database", "Data querying and analysis", 7, 2),
            
            ("Docker", "DevOps", "Container orchestration", 9, 3),
            ("Kubernetes", "DevOps", "Container orchestration", 8, 3),
            ("AWS", "Cloud", "Cloud infrastructure", 8, 3),
            ("Terraform", "Infrastructure", "Infrastructure as Code", 7, 3),
            ("Python", "Programming", "Automation and scripting", 7, 3),
            ("CI/CD", "DevOps", "Continuous integration and deployment", 8, 3),
        ]
        
        for name, category, description, level, user_id in skills:
            cur.execute("SELECT id FROM skill WHERE name = %s AND user_id = %s", (name, user_id))
            if cur.fetchone():
                print(f"      ⚠️  Skill '{name}' already exists for user {user_id}, skipping...")
                continue
            
            cur.execute("""
                INSERT INTO skill (name, category, description, level, user_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """, (name, category, description, level, user_id))
            print(f"      ✅ Created skill: {name} (Level {level}) for user {user_id}")
        
        conn.commit()
        
        print("🎉 Database seeding completed successfully!")
        print("\n🔑 Test credentials:")
        print("   Email: juan.perez@example.com | Password: password123")
        print("   Email: maria.garcia@example.com | Password: password456")
        print("   Email: carlos.lopez@example.com | Password: password789")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("🚀 Database Seeder")
    print("=" * 50)
    seed_database()
