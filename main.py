from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Models
class ServiceRequest(BaseModel):
    customer_name: str
    service_type: str
    description: str
    address: str
    scheduled_date: str

class ServiceResponse(BaseModel):
    request_id: int
    customer_name: str
    service_type: str
    description: str
    address: str
    scheduled_date: str
    status: str

# Mock database
database = []

# Counter for request IDs
request_id_counter = 1

# Endpoints
@app.post("/services/", response_model=ServiceResponse)
def create_service_request(request: ServiceRequest):
    global request_id_counter
    service_request = {
        "request_id": request_id_counter,
        **request.dict(),
        "status": "pending"
    }
    database.append(service_request)
    request_id_counter += 1
    return service_request

@app.get("/services/{request_id}", response_model=ServiceResponse)
def get_service_request(request_id: int):
    for service_request in database:
        if service_request["request_id"] == request_id:
            return service_request
    return {"error": "Service request not found"}

@app.get("/services/", response_model=List[ServiceResponse])
def list_service_requests():
    return database

@app.put("/services/{request_id}", response_model=ServiceResponse)
def update_service_request(request_id: int, update: ServiceRequest):
    for service_request in database:
        if service_request["request_id"] == request_id:
            service_request.update(update.dict())
            return service_request
    return {"error": "Service request not found"}

@app.delete("/services/{request_id}", response_model=dict)
def delete_service_request(request_id: int):
    global database
    database = [sr for sr in database if sr["request_id"] != request_id]
    return {"message": "Service request deleted"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
