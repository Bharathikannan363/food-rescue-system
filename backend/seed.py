import os
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import (
    User, Donor, NGO, Volunteer, Donation,
    Request as FoodRequest, Assignment, Delivery,
    VolunteerLocation, Report, Payment, Log, Notification
)

app = create_app()

def seed_database():
    with app.app_context():
        print("Cleaning and seeding fresh database records...")
        db.drop_all()
        db.create_all()

        # 1. Create Admin User
        admin_user = User(
            username='admin',
            email='admin@foodrescue.org',
            role='ADMIN',
            phone='+919876543210',
            is_approved=True,
            approval_status='APPROVED'
        )
        admin_user.set_password('Admin@123')
        db.session.add(admin_user)

        # 2. Create Donor User & Profile
        donor_user = User(
            username='donor',
            email='donor@hotelgrand.com',
            role='DONOR',
            phone='+919876543211',
            is_approved=True,
            approval_status='APPROVED'
        )
        donor_user.set_password('Donor@123')
        db.session.add(donor_user)
        db.session.flush()

        donor_profile = Donor(
            user_id=donor_user.id,
            organization_name='Grand Palace Hotel & Catering',
            address='123 Hospitality Avenue, Sector 18, City Center',
            latitude=28.6139,
            longitude=77.2090
        )
        db.session.add(donor_profile)

        # 3. Create NGO User & Profile
        ngo_user = User(
            username='ngo',
            email='contact@hopefoundation.org',
            role='NGO',
            phone='+919876543212',
            is_approved=True,
            approval_status='APPROVED'
        )
        ngo_user.set_password('Ngo@123')
        db.session.add(ngo_user)
        db.session.flush()

        ngo_profile = NGO(
            user_id=ngo_user.id,
            ngo_name='Hope & Care Shelter Foundation',
            registration_number='NGO-REG-2024-8890',
            address='45 Compassion Road, Block B, Relief Colony',
            latitude=28.6250,
            longitude=77.2180
        )
        db.session.add(ngo_profile)

        # 4. Create Volunteer User & Profile
        vol_user = User(
            username='volunteer',
            email='alex.volunteer@gmail.com',
            role='VOLUNTEER',
            phone='+919876543213',
            is_approved=True,
            approval_status='APPROVED'
        )
        vol_user.set_password('Volunteer@123')
        db.session.add(vol_user)
        db.session.flush()

        vol_profile = Volunteer(
            user_id=vol_user.id,
            full_name='Alex Rivera',
            vehicle_type='Delivery Van',
            address='78 Green Park Extension, Metro Lane',
            is_available=True,
            latitude=28.6180,
            longitude=77.2130
        )
        db.session.add(vol_profile)

        # Second volunteer - farther from the pickup point (proximity matching demo)
        vol2_user = User(
            username='volunteer2',
            email='priya.volunteer@gmail.com',
            role='VOLUNTEER',
            phone='+919876543214',
            is_approved=True,
            approval_status='APPROVED'
        )
        vol2_user.set_password('Volunteer@123')
        db.session.add(vol2_user)
        db.session.flush()

        vol2_profile = Volunteer(
            user_id=vol2_user.id,
            full_name='Priya Sharma',
            vehicle_type='Scooter',
            address='219 Ridge Road, Civil Lines Quarters',
            is_available=True,
            latitude=28.6250,
            longitude=77.2180
        )
        db.session.add(vol2_profile)

        # Third volunteer - approved but never shared location (no-ping handling demo)
        vol3_user = User(
            username='volunteer3',
            email='ravi.volunteer@gmail.com',
            role='VOLUNTEER',
            phone='+919876543215',
            is_approved=True,
            approval_status='APPROVED'
        )
        vol3_user.set_password('Volunteer@123')
        db.session.add(vol3_user)
        db.session.flush()

        vol3_profile = Volunteer(
            user_id=vol3_user.id,
            full_name='Ravi Kumar',
            vehicle_type='Bike',
            address='54 Ashok Vihar, Phase 2',
            is_available=True,
            latitude=None,
            longitude=None
        )
        db.session.add(vol3_profile)

        db.session.commit()

        # 5. Create Sample Donations
        donation1 = Donation(
            donor_id=donor_profile.id,
            title='Surplus Buffet Meals & Rice Bowls',
            description='Freshly prepared vegetarian rice bowls, dal, and chapati from evening banquet event.',
            food_type='Cooked Meals',
            quantity='60 Meals',
            pickup_address=donor_profile.address,
            latitude=donor_profile.latitude,
            longitude=donor_profile.longitude,
            status='APPROVED'
        )
        donation2 = Donation(
            donor_id=donor_profile.id,
            title='Fresh Bakery Breads & Muffins',
            description='Assorted whole wheat breads, dinner rolls, and fruit muffins baked today.',
            food_type='Bakery Items',
            quantity='35 Packs',
            pickup_address=donor_profile.address,
            latitude=donor_profile.latitude,
            longitude=donor_profile.longitude,
            status='APPROVED'
        )
        now = datetime.utcnow()
        donation1.prep_time = now - timedelta(hours=3)
        donation1.expiry_time = now + timedelta(hours=6)   # FRESH
        donation2.prep_time = now - timedelta(hours=2)
        donation2.expiry_time = now + timedelta(hours=4)   # FRESH
        db.session.add_all([donation1, donation2])

        # Expiry-tracking demo donations (Slide 9/13/14 requirement)
        donation3 = Donation(
            donor_id=donor_profile.id,
            title='Veg Sandwich Packs - Closing Time Sale',
            description='Fresh sandwiches from the evening counter. Best consumed within the hour!',
            food_type='Bakery Items',
            quantity='20 Packs',
            pickup_address=donor_profile.address,
            latitude=donor_profile.latitude,
            longitude=donor_profile.longitude,
            prep_time=now - timedelta(hours=1),
            expiry_time=now + timedelta(minutes=45),   # EXPIRING_SOON (within 2h window)
            status='APPROVED'
        )
        donation4 = Donation(
            donor_id=donor_profile.id,
            title='Evening Chaat & Snacks - Expired Batch',
            description='Leftover chaat from the afternoon stall. Held past its safe consumption window.',
            food_type='Cooked Meals',
            quantity='15 Plates',
            pickup_address=donor_profile.address,
            latitude=donor_profile.latitude,
            longitude=donor_profile.longitude,
            prep_time=now - timedelta(hours=7),
            expiry_time=now - timedelta(hours=2),      # EXPIRED
            status='APPROVED'
        )
        db.session.add_all([donation3, donation4])
        db.session.commit()

        # 6. Create NGO Request
        req1 = FoodRequest(
            donation_id=donation1.id,
            ngo_id=ngo_profile.id,
            status='ACCEPTED',
            quality_status='VERIFIED',
            quality_notes='Verified sealed food containers. Temperature checks optimal.'
        )
        db.session.add(req1)
        donation1.status = 'DONOR_ACCEPTED'
        db.session.commit()

        # 7. Create Volunteer Assignment
        assign1 = Assignment(
            request_id=req1.id,
            volunteer_id=vol_profile.id,
            status='ACCEPTED',
            accepted_at=datetime.utcnow()
        )
        db.session.add(assign1)
        donation1.status = 'VOLUNTEER_ASSIGNED'
        db.session.commit()

        # 8. Create Delivery
        delivery1 = Delivery(
            assignment_id=assign1.id,
            pickup_time=datetime.utcnow() - timedelta(minutes=45),
            pickup_latitude=donor_profile.latitude,
            pickup_longitude=donor_profile.longitude,
            status='OUT_FOR_DELIVERY'
        )
        db.session.add(delivery1)

        # 9. Create Volunteer Initial Locations (live GPS pings for proximity matching)
        vol_loc = VolunteerLocation(
            volunteer_id=vol_profile.id,
            latitude=28.6200,
            longitude=77.2140
        )
        vol2_loc = VolunteerLocation(
            volunteer_id=vol2_profile.id,
            latitude=28.6250,
            longitude=77.2180
        )
        db.session.add_all([vol_loc, vol2_loc])

        # 10. Create Initial Report & Payment & Logs
        rep = Report(
            month='April',
            year=2026,
            total_donations=28,
            total_deliveries=24,
            beneficiaries=480,
            food_saved='70.0 kg'
        )
        pay = Payment(
            transaction_id='TXN-INIT-1001',
            user_id=vol_user.id,
            amount=500.0,
            purpose='Volunteer Logistics Support Grant',
            status='SUCCESS'
        )
        log1 = Log(
            user_id=admin_user.id,
            action="SYSTEM_INIT",
            entity_type="System",
            entity_id=1,
            description="Initialized Food Rescue & Redistribution System Database with Demo Accounts."
        )

        db.session.add_all([rep, pay, log1])
        db.session.commit()

        print("==================================================")
        print(" Database Seeded Successfully!")
        print(" Demo Credentials:")
        print("  - Admin:     username: admin     password: Admin@123")
        print("  - Donor:     username: donor     password: Donor@123")
        print("  - NGO:       username: ngo       password: Ngo@123")
        print("  - Volunteer: username: volunteer password: Volunteer@123")
        print("==================================================")

if __name__ == '__main__':
    seed_database()
