import ast
import json
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Prompt, Tag, EvaluationText, Annotation

def onboard(request):
    return render(request, "onboard.html", {})

def annotate(request):
    text = random.choice(EvaluationText.objects.all())
    sentences = ast.literal_eval(text.body)
    args = {
        "prompt": text.prompt, 
        "text_id": text.pk, 
        "sentences": json.dumps(sentences), 
        "name": request.GET['name'], 
        "max_sentences": len(sentences),
        "boundary": text.boundary
    }
    
    return render(request, "annotate.html", args)

@csrf_exempt
def save(request):  
    text = int(request.POST['text'])
    name = request.POST['name']
    boundary = int(request.POST['boundary'])
    note = request.POST['note']

    grammar = request.POST['grammar'] == 'true'
    repetition = request.POST['repetition'] == 'true'
    entailment = request.POST['entailment'] == 'true'
    sense = request.POST['sense'] == 'true'

    print(grammar, repetition, entailment, sense, note)

    annotation = Annotation.objects.create(
        annotator=name,
        text=EvaluationText.objects.get(pk=text),
        boundary=boundary,
        note=note
    )

    if grammar: annotation.tags.add(Tag.objects.get(name="grammar"))
    if repetition: annotation.tags.add(Tag.objects.get(name="repetition"))
    if entailment: annotation.tags.add(Tag.objects.get(name="entailment"))
    if sense: annotation.tags.add(Tag.objects.get(name="sense"))
    annotation.save()

    return JsonResponse({'status': 200})