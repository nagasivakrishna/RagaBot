import os
import youtube_dl

ydl_opts2 = {
        'format': 'bestaudio/best',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
      }

def Parallel_Download(i):
  print("----------------------------------------------")
  print("[LOG] Moved to Parallel_Download * * * * * * * * ")
  try:
    if not os.path.isfile(f"./FILES/{i[24:]}.mp3"):
      with youtube_dl.YoutubeDL(ydl_opts2) as ydl2:
        try:
          print(i)
          ydl2.download([i])
          print("\n[YDL-2] Download complete with ydl2")
        except:
          print("[ERROR] Age ristricted video, returning 0 status")
          return
      
      ### renaming the unwanted files
      print("[LOG] Removing the unwanted files")
      for file in os.listdir("./"):
        if file.endswith(".webm") or file.endswith(".m4a") or file.endswith(".mp4"):
          os.rename(file,f"./FILES/{i[24:]}.mp3")
          print("[CLEANING] Succesful")
        else:
          pass

      for file2 in os.listdir("./"):
        if file2.endswith(".mp3"):
          os.rename(file2, f"./FILES/{i[24:]}.mp3")
          print(f"[LOG] Song renamed and is successfully added to DB with name {i[24:]}.mp3")
        else:
          pass
      
      
        
    else:
      print("[LOG] Song exists. ready to play next!")
  except:
    print("[LOG] Error occured at check_download")