from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title='API Create phiếu đăng ký khóa học',
    description='API Create phiếu đăng ký khóa học',
    version='1.0.0'
)

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]
courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]
registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int
    
@app.post("/registrations", status_code=201)
def create_registration(registration: RegistrationCreate):
    student_exists = False
    for student in students:
        if student["id"] == registration.student_id:
            student_exists = True
            break
        
    if not student_exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )
        
    course = None
    for c in courses:
        if c["id"] == registration.course_id:
            course = c
            break
        
    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy khóa học"
        )
    
    for item in registrations:
        if (item["student_id"] == registration.student_id and item["course_id"] == registration.course_id):
            raise HTTPException(
                status_code=400,
                detail="Sinh viên đã đăng kí khóa học này"
            )
            
    count = 0
    for item in registrations:
        if item["course_id"] == registration.course_id:
            count += 1
            
    if count >= courses["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đủ số lượng sinh viên"
        )
        
    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }
    
    registrations.append(new_registration)
    
    return {
        "message": "Đăng kí khóa học thành công",
        "data": new_registration
    }