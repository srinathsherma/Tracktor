# seed.py
# Run this script to populate the database with sample data
# Usage: python seed.py

from app import app
from models import db, Technician, Category, Ticket
from datetime import datetime, timezone, timedelta

def seed_database():
    with app.app_context():

        # ── Check if data already exists ──────────────────────────
        if Technician.query.first():
            print("⚠️  Database already has data!")
            answer = input("Do you want to clear it and reseed? (yes/no): ")
            if answer.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return

            # Clear existing data in correct order
            print("🗑️  Clearing existing data...")
            Ticket.query.delete()
            Technician.query.delete()
            Category.query.delete()
            db.session.commit()
            print("✅ Existing data cleared!")

        # ── Seed technicians ──────────────────────────────────────
        print("\n👷 Adding technicians...")
        technicians = [
            Technician(
                name        = 'Alice Nguyen',
                email       = 'alice.nguyen@example.com',
                phone       = '+61 400 111 222',
                job_title   = 'Senior Technician',
                department  = 'Infrastructure',
                bio         = 'Alice specialises in network infrastructure and server management with over 8 years of experience.',
                date_joined = datetime.now(timezone.utc) - timedelta(days=365)
            ),
            Technician(
                name        = 'Bob Tremblay',
                email       = 'bob.tremblay@example.com',
                phone       = '+61 400 333 444',
                job_title   = 'IT Support Specialist',
                department  = 'Software',
                bio         = 'Bob is our go-to person for software issues and application support across the organisation.',
                date_joined = datetime.now(timezone.utc) - timedelta(days=270)
            ),
            Technician(
                name        = 'Carol Singh',
                email       = 'carol.singh@example.com',
                phone       = '+61 400 555 666',
                job_title   = 'Hardware Technician',
                department  = 'Hardware',
                bio         = 'Carol handles all hardware repairs, equipment setup and physical infrastructure maintenance.',
                date_joined = datetime.now(timezone.utc) - timedelta(days=180)
            ),
            Technician(
                name        = 'David Okafor',
                email       = 'david.okafor@example.com',
                phone       = '+61 400 777 888',
                job_title   = 'Security Specialist',
                department  = 'Access & Security',
                bio         = 'David manages user access, security policies and compliance across all systems.',
                date_joined = datetime.now(timezone.utc) - timedelta(days=90)
            ),
        ]
        db.session.add_all(technicians)
        db.session.commit()
        print(f"✅ Added {len(technicians)} technicians!")

        # ── Seed categories ───────────────────────────────────────
        print("\n📁 Adding categories...")
        categories = [
            Category(
                name        = 'Software defect',
                description = 'Bugs, crashes and application errors'
            ),
            Category(
                name        = 'Operating system',
                description = 'OS faults, updates and boot issues'
            ),
            Category(
                name        = 'Hardware',
                description = 'Physical device failures and peripherals'
            ),
            Category(
                name        = 'Network',
                description = 'Connectivity, VPN and Wi-Fi issues'
            ),
            Category(
                name        = 'Access & security',
                description = 'Passwords, permissions and accounts'
            ),
            Category(
                name        = 'New setup',
                description = 'New equipment or user onboarding'
            ),
        ]
        db.session.add_all(categories)
        db.session.commit()
        print(f"✅ Added {len(categories)} categories!")

        # ── Seed tickets ──────────────────────────────────────────
        print("\n🎫 Adding tickets...")
        tickets = [
            Ticket(
                title         = 'Printer not responding',
                description   = 'The shared printer on level 2 is offline. Staff cannot print documents.',
                status        = 'open',
                priority      = 'high',
                technician_id = None,
                category_id   = 3,
                notes         = None,
                date_requested = datetime.now(timezone.utc) - timedelta(days=5),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
            Ticket(
                title         = 'Email client crash on startup',
                description   = 'Outlook crashes immediately on launch for user Jane Smith. Tried reinstalling — issue persists.',
                status        = 'open',
                priority      = 'critical',
                technician_id = None,
                category_id   = 1,
                notes         = None,
                date_requested = datetime.now(timezone.utc) - timedelta(days=2),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
            Ticket(
                title         = 'Laptop running slowly',
                description   = 'User reports laptop has become very slow over the past week. Suspect malware or full disk.',
                status        = 'in_progress',
                priority      = 'high',
                technician_id = 1,
                category_id   = 1,
                notes         = 'Initial scan running. Disk at 98% capacity — clearing temp files.',
                date_requested = datetime.now(timezone.utc) - timedelta(days=7),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
            Ticket(
                title         = 'VPN not connecting from home',
                description   = 'Remote staff member cannot connect to the VPN. Error code 800 returned.',
                status        = 'in_progress',
                priority      = 'critical',
                technician_id = 2,
                category_id   = 4,
                notes         = 'Confirmed firewall rule issue on the users home router. Awaiting router access.',
                date_requested = datetime.now(timezone.utc) - timedelta(days=3),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
            Ticket(
                title         = 'New monitor setup required',
                description   = 'New hire in the accounts team needs a second monitor configured at their workstation.',
                status        = 'in_progress',
                priority      = 'medium',
                technician_id = 3,
                category_id   = 6,
                notes         = 'Monitor delivered. Waiting on correct DisplayPort cable to arrive.',
                date_requested = datetime.now(timezone.utc) - timedelta(days=1),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
            Ticket(
                title         = 'Password reset request',
                description   = 'User locked out of their account after too many failed login attempts.',
                status        = 'closed',
                priority      = 'low',
                technician_id = 4,
                category_id   = 5,
                notes         = 'Password reset completed. User advised to use password manager.',
                date_requested = datetime.now(timezone.utc) - timedelta(days=10),
                date_completed = datetime.now(timezone.utc) - timedelta(days=10) + timedelta(hours=2),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
            Ticket(
                title         = 'Software installation — Adobe Acrobat',
                description   = 'Finance team requires Adobe Acrobat Pro installed on 3 workstations.',
                status        = 'closed',
                priority      = 'medium',
                technician_id = 1,
                category_id   = 1,
                notes         = 'Installed on all 3 machines. Licences applied and verified.',
                date_requested = datetime.now(timezone.utc) - timedelta(days=14),
                date_completed = datetime.now(timezone.utc) - timedelta(days=13),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
            Ticket(
                title         = 'Network drop in meeting room B',
                description   = 'Ethernet connection in meeting room B intermittent. Affects video calls.',
                status        = 'closed',
                priority      = 'high',
                technician_id = 2,
                category_id   = 4,
                notes         = 'Faulty patch cable replaced. Connection stable — tested over 30 minutes.',
                date_requested = datetime.now(timezone.utc) - timedelta(days=20),
                date_completed = datetime.now(timezone.utc) - timedelta(days=19),
                created_at    = datetime.now(timezone.utc),
                updated_at    = datetime.now(timezone.utc)
            ),
        ]
        db.session.add_all(tickets)
        db.session.commit()
        print(f"✅ Added {len(tickets)} tickets!")

        # ── Done ──────────────────────────────────────────────────
        print("\n🚜 Tracktor database seeded successfully!")
        print("=" * 50)
        print(f"   👷 {len(technicians)} technicians")
        print(f"   📁 {len(categories)} categories")
        print(f"   🎫 {len(tickets)} tickets")
        print("=" * 50)
        print("\n🌐 Run python app.py to start Tracktor!")

if __name__ == '__main__':
    seed_database()