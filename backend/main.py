


from fastapi import FastAPI                # FastAPI creates the server
from fastapi.middleware.cors import CORSMiddleware  # allows frontend to talk to backend
from backend.api.routes import router      # import all our endpoints



# Create the FastAPI app


app = FastAPI(
    title       = "Research Assistant API",   # name shown in docs
    description = "Multi Agent Research Tool", # description in docs
    version     = "1.0.0"
)



# STEP 2 — Add CORS Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],   # allow all origins (fine for local dev)
    allow_methods     = ["*"],   # allow all methods (GET, POST, etc)
    allow_headers     = ["*"],   # allow all headers
)


# STEP 3 — Connect all routes


app.include_router(router)


#  Run directly (optional)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)