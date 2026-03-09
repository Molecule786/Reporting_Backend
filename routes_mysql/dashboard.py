from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models_mysql.report import Report
from models_mysql.task import Task
from utils.mysql_db import get_db
from utils.auth import get_current_user

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = int(current_user.get("user_id"))
        user_role = current_user.get("role")
        
        if user_role == "admin":
            total_reports = db.query(Report).count()
            total_tasks = db.query(Task).count()
            pending_reports = db.query(Report).filter(Report.status == "pending").count()
            pending_tasks = db.query(Task).filter(Task.status == "pending").count()
        else:
            total_reports = db.query(Report).filter(Report.user_id == user_id).count()
            total_tasks = db.query(Task).filter(Task.user_id == user_id).count()
            pending_reports = db.query(Report).filter(Report.user_id == user_id, Report.status == "pending").count()
            pending_tasks = db.query(Task).filter(Task.user_id == user_id, Task.status == "pending").count()
        
        return {
            "success": True,
            "data": {
                "my_reports": total_reports,
                "my_tasks": total_tasks,
                "pending_reports": pending_reports,
                "pending_tasks": pending_tasks
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
