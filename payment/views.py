# views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
import razorpay
from accounts.models import Order, Course
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreatePayment(View):
    def post(self, request):
        student_id = request.POST['student_id']
        cart_items = request.POST.getlist('cart_items[]')
        

        total_amount = 0
        for item in cart_items:
            course = Course.objects.get(id=item)
            total_amount += float(course.course_fee)
        total_amount_paise = total_amount * 100

        razorpay_order = razorpay_client.order.create({
            "amount": total_amount_paise,
            "currency": "INR",
            "payment_capture": "1"
        })
        request.session['razorpay_order_id'] = razorpay_order['id']
        request.session['student_id'] = student_id
        request.session['cart_items'] = cart_items

       
        return render(request, 'checkout.html', {
            'order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'total_amount': total_amount
        })

@method_decorator(csrf_exempt, name='dispatch')
class VerifyPayment(View):
    def post(self, request):
        # Get Razorpay payment details
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.session.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        student_id = request.session.get('student_id')
        cart_items = request.session.get('cart_items', [])
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            for item in cart_items:
                course = Course.objects.get(id=item)
                Order.objects.create(student_id=student_id, course=course, status='Completed')
            request.session.pop('razorpay_order_id', None)
            request.session.pop('cart_items', None)
            return redirect('cart')  
        except razorpay.errors.SignatureVerificationError:
            return redirect('cart')  
