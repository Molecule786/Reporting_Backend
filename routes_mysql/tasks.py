from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models_mysql.task import Task, TaskCreate, TaskUpdate
from models_mysql.user import User
from utils.mysql_db import get_db
from utils.auth import get_current_user
import json

router = APIRouter()

@router.post("/")
@router.post("")
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        # Only admins can create tasks
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create tasks"
            )
        
        # Safely convert user_id to int
        user_id_val = current_user.get("user_id")
        if user_id_val is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token"
            )
        admin_id = int(str(user_id_val))
        
        db_task = Task(
            user_id=task.user_id,
            assigned_by=admin_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date,
            attachments=json.dumps(task.attachments) if task.attachments else json.dumps([]),
            voice_notes=json.dumps(task.voice_notes) if task.voice_notes else json.dumps([]),
            status="pending"
        )
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        return {
            "success": True,
            "message": "Task created successfully",
            "data": {"task_id": db_task.id}
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/")
@router.get("")
def get_tasks(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        # Safely convert user_id to int
        user_id_val = current_user.get("user_id")
        if user_id_val is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token"
            )
        user_id = int(str(user_id_val))
        user_role = current_user.get("role")
        
        if user_role == "admin":
            tasks = db.query(Task).order_by(desc(Task.created_at)).all()
        else:
            tasks = db.query(Task).filter(Task.user_id == user_id).order_by(desc(Task.created_at)).all()
        
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                "_id": str(task.id),
                "user_id": str(task.user_id),
                "assigned_by": str(task.assigned_by) if task.assigned_by else None,
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                "status": task.status.value if hasattr(task.status, 'value') else task.status,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "attachments": json.loads(task.attachments) if isinstance(task.attachments, str) else task.attachments,
                "voice_notes": json.loads(task.voice_notes) if isinstance(task.voice_notes, str) else task.voice_notes,
                "created_at": task.created_at.isoformat() if task.created_at else None
            })
        
        return {
            "success": True,
            "data": {"tasks": tasks_list}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update fields
        if task_update.title:
            task.title = task_update.title
        if task_update.description:
            task.description = task_update.description
        if task_update.priority:
            task.priority = task_update.priority
        if task_update.status:
            task.status = task_update.status
        if task_update.due_date:
            task.due_date = task_update.due_date
        if task_update.attachments is not None:
            task.attachments = json.dumps(task_update.attachments)
        if task_update.voice_notes is not None:
            task.voice_notes = json.dumps(task_update.voice_notes)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Task updated successfully"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete tasks"
            )
        
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        db.delete(task)
        db.commit()
        
        return {
            "success": True,
            "message": "Task deleted successfully"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
