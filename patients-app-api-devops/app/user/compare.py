from facepplib import FacePP ,exceptions


# define global variables
face_detection = ""
faceset_initialize = ""
face_search = ""
face_landmarks = ""
dense_facial_landmarks = ""
face_attributes = ""
beauty_score_and_emotion_recognition = ""
face_comparing_localphoto = ""
face_comparing_websitephoto = ""

# api details
api_key ='xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
api_secret ='TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'

# define face comparing function
def face_comparing(Image1, Image2):
    

    app = FacePP(api_key = api_key, api_secret = api_secret)
    funcs = [
        face_detection,
        face_comparing_localphoto,
        face_comparing_websitephoto,
        faceset_initialize,
        face_search,
        face_landmarks,
        dense_facial_landmarks,
        face_attributes,
        beauty_score_and_emotion_recognition
    ]

    print()
    print('-'*30)
    print('Comparing Photographs......')
    print('-'*30)
  
   
    cmp_ = app.compare.get(image_url1 = Image1,
                           image_url2 = Image2)
   
    print('Photo1', '=', cmp_.image1)
    print('Photo2', '=', cmp_.image2)
   
    # Comparing Photos
    if cmp_.confidence > 70:
        print('Both photographs are of same person......')
        return "Same"
    else:
        print('Both photographs are of two different persons......')
        return "Different"