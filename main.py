from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ----------------------------------------------------------------
# 1. ĐỊNH NGHĨA MODEL (Pydantic) jhuvjvh
# ----------------------------------------------------------------
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

class UserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    message: Optional[str] = None

# ----------------------------------------------------------------
# 2. "CƠ SềEDỮ LIềE" GIẢ LẬP BẰNG LIST
# ----------------------------------------------------------------
# Sử dụng List bình thường đềElưu dữ liệu thay vì dùng Database
tasks_db: List[Task] = []

# ----------------------------------------------------------------
# 3. CÁC API ENDPOINT (CRUD: Create, Read, Update, Delete)
# ----------------------------------------------------------------

# GET: Lấy danh sách tất cả công việc
@app.get("/")
def read_root():
    return {"Hello": "Branch B"}

@app.get("/tasks")
def get_tasks():
    return tasks_db

# POST: Tạo một công việc mới
@app.post("/tasks")
def create_task(task: Task):
    # (Tùy chọn) Kiểm tra xem ID có bềEtrùng không
    for existing_task in tasks_db:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="ID công việc đã tồn tại!")
            
    # Thêm công việc mới vào danh sách
    tasks_db.append(task)
    return {"message": "Tạo công việc thành công!", "task": task}

# PUT: Chỉnh sửa/Cập nhật toàn bềEmột công việc dựa vào ID
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, existing_task in enumerate(tasks_db):
        # Tìm xem công việc nào có id khớp với task_id truyền vào
        if existing_task.id == task_id:
            # Thay thế công việc cũ bằng công việc mới
            tasks_db[index] = updated_task
            return {"message": "Cập nhật thành công!", "task": updated_task}
            
    # Nếu vòng lặp chạy hết mà không tìm thấy ID thì báo lỗi
    raise HTTPException(status_code=404, detail="Không tìm thấy công việc đềEcập nhật")

# DELETE: Xóa một công việc dựa vào ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, existing_task in enumerate(tasks_db):
        if existing_task.id == task_id:
            # Xóa phần tử khỏi danh sách
            del tasks_db[index]
            return {"message": f"Đã xóa công việc có ID {task_id}"}
            
    raise HTTPException(status_code=404, detail="Không tìm thấy công việc đềExóa")
