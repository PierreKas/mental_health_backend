
import joblib
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def depression_predict(request):
    try:
        cls= joblib.load('phq_9_model.joblib')
        data= request.data
        required_fields= ['phq' + str(i) for i in range (1,10)]
        if not all(field in data for field in required_fields):
            return Response({
                'error': 'Missing required fields',
                'required_fields': required_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        lis = [int(data[field]) for field in required_fields]
        
        answer= cls.predict([lis])[0]

        if 0 <= answer <= 4:
            message = "Minimal depression"
        elif 5 <= answer <= 14:
            message = "Mild to moderate depression"
        elif 15 <= answer <= 19:
            message = "Moderately severe depression"
        elif answer >= 20:
            message = "Severe depression"
        else:
            message = "Invalid prediction result"

        return Response({
            'inputs': lis,
            'result': message,
            'prediction_score': int(answer)
        },status=status.HTTP_200_OK)
    
    except ValueError as e:
        return Response({
            'error': 'Invalid input values. All vaues must be integers between 0 and 3'
        })


    except Exception as e:
        return Response({
            'error': str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)