import os
import uuid
import torch
from diffusers import StableDiffusionPipeline, DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from PIL import Image
import database
import time
from datetime import datetime, timedelta

class CFG:
    device = "cuda" if torch.cuda.is_available() else "cpu"  # Use "cuda" if GPU is available
    seed = 42
    generator = torch.manual_seed(seed)
    image_gen_steps = 20  # Reduced steps for speed
    image_gen_model_id = "runwayml/stable-diffusion-v1-5"  # Model ID for Image generation
    image_gen_size = (512, 512)  # Can lower the size for speed
    image_gen_guidance_scale = 7
    prompt_dataset_size = 1  # Number of images/videos to generate
    video_gen_model_id = "damo-vilab/text-to-video-ms-1.7b"  # Model ID for video generation
    video_gen_steps = 5
    video_duration_seconds = 3
    video_gen_frames = video_duration_seconds * 10

# Load Stable Diffusion model for images
try:
    if (torch.cuda.is_available()==True):
        image_gen_model = StableDiffusionPipeline.from_pretrained(
        CFG.image_gen_model_id,
        torch_dtype=torch.float16,
        variant='fp16',
    ).to(CFG.device)

    else:
        image_gen_model = StableDiffusionPipeline.from_pretrained(
        CFG.image_gen_model_id,
        torch_dtype=torch.float32,
    ).to(CFG.device)
except Exception as e:
    print(f"Error loading image model: {e}")
    exit()

# Load a DiffusionPipeline for video generation
try:
    if (torch.cuda.is_available()==True):
        video_gen_model = DiffusionPipeline.from_pretrained(
        CFG.video_gen_model_id,
        torch_dtype=torch.float16,
        variant='fp16',
    ).to(CFG.device)
        video_gen_model.scheduler = DPMSolverMultistepScheduler.from_config(video_gen_model.scheduler.config)
        # optimize for GPU memory
        video_gen_model.enable_model_cpu_offload()
        video_gen_model.enable_vae_slicing()
    else:
        video_gen_model = DiffusionPipeline.from_pretrained(
        CFG.video_gen_model_id,
        torch_dtype=torch.float32,
    ).to(CFG.device)
    video_gen_model.scheduler = DPMSolverMultistepScheduler.from_config(video_gen_model.scheduler.config)

except Exception as e:
    print(f"Error loading video model: {e}")
    exit()

def generate_image(prompt, index):
    """Generates and saves a single image."""
    try:
        print(f"Generating image {index + 1}...")
        image = image_gen_model(
            prompt,
            num_inference_steps=CFG.image_gen_steps,
            guidance_scale=CFG.image_gen_guidance_scale
        ).images[0]

        # Resize to desired dimensions
        image.thumbnail(CFG.image_gen_size)

        # Save image locally
        image_path = f"image_{index + 1}.png"
        image.save(image_path)
        print(f"Image {index + 1} saved to {image_path}")
        return image_path
    except Exception as e:
        print(f"Error generating image {index + 1}: {e}")
        return None

def generate_video_with_diffusers(prompt, index):
    """Generates a video using the Diffusers pipeline."""
    try:
        print(f"Generating video for prompt: {prompt}")
        video_frames = video_gen_model(prompt, negative_prompt="low quality", num_inference_steps=CFG.video_gen_steps, num_frames=CFG.video_gen_frames).frames
        video_frames = video_frames[0]
        # Convert frames to video
        video_path = f"video_{index + 1}.mp4"
        print(f"Converting frames to video: {video_path}")
        video_path = export_to_video(video_frames)
        print(f"Video saved to: {video_path}")
        return video_path
    except Exception as e:
        print(f"Error generating video: {e}")
        return None

def save_content_to_user_directory(user_id, images, videos):
    """Save generated content into a user-specific directory."""
    base_dir = f"static/generated_content/{user_id}"
    os.makedirs(base_dir, exist_ok=True)

    # Move images
    for img in images:
        if img:
            os.rename(img, os.path.join(base_dir, os.path.basename(img)))

    # Move videos
    for vid in videos:
        if vid:
            os.rename(vid, os.path.join(base_dir, os.path.basename(vid)))

    return base_dir

def main():
    prompt = input("Enter a text prompt for content generation: ").strip()

    user_id = str(uuid.uuid4())  # Generate unique user_id

    print("Your unique user id is: "+ user_id)

    print("Your promt is: " + prompt)

    # Ask the user for a notification time
    notify_time_input = input("Enter notification time in HH:MM (24-hour format, leave empty for immediate notification): ").strip()

    # Calculate the notification time or default to "immediate"
    if notify_time_input:
        notify_time = datetime.strptime(notify_time_input, "%H:%M").replace(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
    else:
        notify_time = None

    # Insert the initial record into the database with status "Processing"
    database.insert_record(user_id, prompt, status="Processing")

    print("Generating videos using Diffusers...")
    generated_videos = [generate_video_with_diffusers(prompt, i) for i in range(CFG.prompt_dataset_size)]

    #generated_videos = 'NA'

    print("Generating images using Stable Diffusion...")
    generated_images = [generate_image(prompt, i) for i in range(CFG.prompt_dataset_size)]

    # Save all content in the user-specific directory
    output_dir = save_content_to_user_directory(user_id, generated_images, generated_videos)
    print(f"Generated content saved in: {output_dir}")

    image_paths = [
        f"generated_content/{user_id}/{os.path.basename(img)}" if img else "Not generated"
        for img in generated_images
    ]

    video_paths = [
        f"generated_content/{user_id}/{os.path.basename(vid)}" if vid else 'Not generated'
        for vid in generated_videos
    ]

    # Update the database with paths to the generated content and set status to "Completed"
    database.update_record(user_id, video_paths, image_paths, status="Completed")

    database.log_activity(user_id, "Generated content")  # Log content generation activity

    # Wait until the specified notification time or notify immediately
    current_time = datetime.now()
    if notify_time and notify_time > current_time:
        wait_seconds = (notify_time - current_time).total_seconds()
        print(f"Notification scheduled for {notify_time.strftime('%H:%M')}. Waiting...")
        time.sleep(wait_seconds)

    print(f"Content is ready! Visit: http://127.0.0.1:5000")

if __name__ == "__main__":
    main()