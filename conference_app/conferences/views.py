from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Conference, Like


# 	Sukurkite ListView, kuris atvaizduotų visas konferencijas
class ConferenceListView( ListView ):
    model = Conference

# Alternatyva ListView klasei:
# def conference_list( request ):
#     conferences = Conference.objects.all()
#     return render( request, "conferences/conference_list.html", { "object_list": conferences })

class ConferenceDetailView( DetailView ):
    model = Conference

# Alternatyva DetailView
# def conference_detail( request, pk ): # pk ateina iš urls failo: path( "<int:pk>/", ... )
#     conference = get_object_or_404( Conference, pk = pk )
#     return render( request, "conferences/conference_detail.html", { "object": conference } )

class ConferenceLikeView( View ):
    def get(self, request, konferencijos_id, conference):
        if not request.user.is_authenticated:
            return redirect( 'login' )

        event = get_object_or_404(Conference, id=konferencijos_id)

        like_kiekis = Like.objects.filter(
            conference=conference, user=request.user).count()

        # SELECT COUNT(*) FROM event_registration WHERE
        # event_id = 1 AND user_id = 1;

        if like_kiekis > 0:
            return HttpResponse("Jūs jau prisiregistravote!")

        registration = Like()
        registration.conference = conference
        registration.user = request.user
        registration.save()
        return redirect("conference-detail", konferencijos_id)