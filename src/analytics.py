from models import db, Student, Company, Interview, Offer

def generate_placement_statistics():
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_interviews = Interview.query.count()
    total_offers = Offer.query.count()
    
    placed_students = Offer.query.filter_by(status='Accepted').count()
    company_success_rate = (placed_students / total_students) * 100 if total_students > 0 else 0

    return {
        'total_students': total_students,
        'total_companies': total_companies,
        'total_interviews': total_interviews,
        'total_offers': total_offers,
        'placed_students': placed_students,
        'company_success_rate': company_success_rate
    }

def track_student_performance(student_usn):
    interviews = Interview.query.filter_by(student_usn=student_usn).all()
    offers = Offer.query.filter_by(student_usn=student_usn).all()
    
    return {
        'interview_count': len(interviews),
        'offers_received': len(offers)
    } 