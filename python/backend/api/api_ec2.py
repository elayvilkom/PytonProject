from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
# from python.backend.script import instance  # זה המקום שבו הגדרת את הפונקציות שלך
from python import instance
app = FastAPI()
# router = APIRouter()

# מודל עבור בקשת יצירת EC2
class EC2CreateRequest(BaseModel):
    instance_name: str
    size_type: str
    ami_types: str

# מודל עבור בקשת מזהה אינסטנס
class InstanceIdentifierRequest(BaseModel):
    instance_identifier: str

@router.post("/createInstance")
async def create_ec2(request: EC2CreateRequest):
    try:
        # קריאה לפונקציה catalog_choice, שתעשה את כל ההתאמות וההגדרות
        result = instance.catalog_choice(
            instance_name=request.instance_name, 
            size_type=request.size_type, 
            ami_types=request.ami_types
        )
        
        # אם לא חזרו תוצאות תקינות, מעלה חריגה
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # החזרת תוצאות בהצלחה
        return {
            "instance_id": result["id"], 
            "instance_name": result["name"], 
            "public_ip": result["public_ip"],
            "message": result["message"]
        }
    
    except Exception as e:
        # אם קרתה שגיאה כלשהי בתהליך
        raise HTTPException(status_code=500, detail=str(e))

# הוספת פונקציות נוספות אם צריך, כמו הפעלת EC2, עצירתו ומחיקתו:
@router.post("/startInstance")
async def start_instance(request: InstanceIdentifierRequest):
    try:
        result = instance.start_ec2(request.instance_identifier)
        return {"message": f"Instance {request.instance_identifier} started successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stopInstance")
async def stop_instance(request: InstanceIdentifierRequest):
    try:
        result = instance.stop_ec2(request.instance_identifier)
        return {"message": f"Instance {request.instance_identifier} stopped successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/deleteInstance")
async def delete_instance(request: InstanceIdentifierRequest):
    try:
        result = instance.delete_ec2(request.instance_identifier)
        return {"message": f"Instance {request.instance_identifier} deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# דוגמה למודל שמחזיר את כל ה-Instances שלך
@router.get("/listInstances")
async def list_instances():
    try:
        result = instance.list_ec2()  # פונקציה להחזיר את כל ה-Instances
        return {"instances": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
