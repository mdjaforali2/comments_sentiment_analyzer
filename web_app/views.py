# web_app/views.py
from django.shortcuts import render
from .forms import CommentForm
from .sentiment_analyzer import analyze_sentiment_with_plot
from .models import Comment
from django.contrib import messages

def home(request):
    return render(request, 'home.html')


# views.py

def analyze_and_save_comment(comment_text):
    try:
        sentiment, sentiment_probabilities, image_base64 = analyze_sentiment_with_plot(comment_text)

        # Save the comment and sentiment analysis results to the database
        comment = Comment(
            comment_text=comment_text,
            sentiment=sentiment,
            probability_positive=sentiment_probabilities[1],  # Adjust based on your model
            probability_negative=sentiment_probabilities[0],  # Adjust based on your model
        )
        comment.save()

        return sentiment, image_base64
    except Exception as e:
        # Handle exceptions, log errors, or take appropriate action
        print(f"Error during sentiment analysis and comment saving: {e}")
        return None, None


def product_page(request):
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            sentiment, sentiment_probabilities, image_base64 = analyze_sentiment_with_plot(comment_text)

            # Save the comment and sentiment analysis results to the database
            comment = Comment(
                comment_text=comment_text,
                sentiment=sentiment,
                probability_positive=sentiment_probabilities[1],  # Adjust based on your model
                probability_negative=sentiment_probabilities[0], # Assign True for Negative, False for Positive
            )
            comment.save()
            form = CommentForm()
            messages.success(request, 'Comment submitted successfully!')
            return render(request, 'product_page.html', {'form': form, 'sentiment': sentiment, 'image_base64': image_base64, 'comment_saved': True})
    return render(request, 'product_page.html', {'form': form})



# views.py
def comment_history(request):
    comments = Comment.objects.all()
    return render(request, 'comment_history.html', {'comments': comments})
