from fastapi import FastAPI
from pydantic import BaseModel
import random
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

class RoomInput(BaseModel):
    width: int
    height: int
    furniture: list[str]

@app.post("/arrange_furniture/")
def arrange_furniture(input_data: RoomInput):
    layout = {}
    
    for item in input_data.furniture:
        layout[item] = {
            "x": round(random.uniform(0, input_data.width), 2),
            "y": round(random.uniform(0, input_data.height), 2)
        }
    
    # Generate visualization
    img_data = generate_room_visual(input_data.width, input_data.height, layout)
    
    return {"layout": layout, "image": img_data}

def generate_room_visual(width, height, layout):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title("Furniture Layout")
    
    # Draw furniture
    for item, pos in layout.items():
        ax.scatter(pos["x"], pos["y"], label=item, s=100)
        ax.text(pos["x"], pos["y"], item, fontsize=12, ha='right')

    ax.legend()
    
    # Convert plot to base64 image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close(fig)
    img_buffer.seek(0)
    
    return base64.b64encode(img_buffer.read()).decode("utf-8")
