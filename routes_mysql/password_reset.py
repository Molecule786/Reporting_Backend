from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password():
    return {
        "success": True,
        "message": "Password reset email sent"
    }

@router.post("/reset-password")
async def reset_password():
    return {
        "success": True,
        "message": "Password reset successfully"
    }
