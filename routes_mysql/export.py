from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.mysql_db import get_db
from utils.auth import get_current_user
from models_mysql.report import Report
from models_mysql.task import Task
from models_mysql.leave import Leave
from models_mysql.user import User
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/export/reports")
async def export_reports(format: str = "csv", db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        if format.lower() != "csv":
            return {
                "success": False,
                "message": "Only CSV format is currently supported"
            }
        
        # Get all reports with user data
        reports = db.query(Report).all()
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            "ID", "User ID", "User Name", "Project Name", "Project Code", 
            "Description", "Status", "Created At", "Updated At"
        ])
        
        # Write data
        for report in reports:
            writer.writerow([
                report.id,
                report.user_id,
                report.user_name,
                report.project_name,
                report.project_code or "",
                report.description,
                report.status.value if hasattr(report.status, 'value') else report.status,
                report.created_at.isoformat() if report.created_at else "",
                report.updated_at.isoformat() if report.updated_at else ""
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=reports.csv"}
        )
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Export failed: {str(e)}"
        }

@router.get("/export/tasks")
async def export_tasks(format: str = "csv", db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        if format.lower() != "csv":
            return {
                "success": False,
                "message": "Only CSV format is currently supported"
            }
        
        # Get all tasks and users separately
        tasks = db.query(Task).all()
        users = {user.id: user for user in db.query(User).all()}
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            "ID", "User ID", "User Name", "User Email", "Title", "Description", 
            "Status", "Priority", "Due Date", "Created At", "Updated At"
        ])
        
        # Write data
        for task in tasks:
            user = users.get(task.user_id)
            writer.writerow([
                task.id,
                task.user_id,
                user.full_name if user else "Unknown",
                user.email if user else "Unknown",
                task.title,
                task.description or "",
                task.status.value if hasattr(task.status, 'value') else task.status,
                task.priority.value if hasattr(task.priority, 'value') else task.priority,
                task.due_date.isoformat() if task.due_date else "",
                task.created_at.isoformat() if task.created_at else "",
                task.updated_at.isoformat() if task.updated_at else ""
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tasks.csv"}
        )
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Export failed: {str(e)}"
        }

@router.get("/export/leaves")
async def export_leaves(format: str = "csv", db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        if format.lower() != "csv":
            return {
                "success": False,
                "message": "Only CSV format is currently supported"
            }
        
        # Get all leaves
        leaves = db.query(Leave).all()
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            "ID", "User ID", "User Name", "User Email", "Leave Type", "Reason", 
            "Start Date", "End Date", "Status", "Admin Comment", "Created At"
        ])
        
        # Write data
        for leave in leaves:
            writer.writerow([
                leave.id,
                leave.user_id,
                leave.user_name,
                leave.user_email,
                leave.leave_type,
                leave.reason,
                leave.start_date.isoformat() if leave.start_date else "",
                leave.end_date.isoformat() if leave.end_date else "",
                leave.status.value if hasattr(leave.status, 'value') else leave.status,
                leave.admin_comment or "",
                leave.created_at.isoformat() if leave.created_at else ""
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=leaves.csv"}
        )
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Export failed: {str(e)}"
        }
