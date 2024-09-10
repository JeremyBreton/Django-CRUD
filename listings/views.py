# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from listings.models import Band, Listing
from listings.forms import ContactUsForm, BandForm, ListingsForm
from django.core.mail import send_mail

def band_list(request):
    bands = Band.objects.all()
    return render(request, 'listings/band_list.html',
                  context={'bands': bands})


def band_detail(request, band_id):
    band = Band.objects.get(id=band_id)
    return render(request, 'listings/band_detail.html',
                  {'band': band})


def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            # Créer une nouvelle "Band" et la sauvegarder dans la database
            band = form.save()
            # Redirige vers la page de détail du groupe que nous venons de créer
            # On peut fournir les arguements du motif url comme arguments à la fonction de redirection
            return HttpResponseRedirect(reverse('band-detail', kwargs={'band_id': band.id}))
    else:
        form = BandForm()

    return render(request, 'listings/band_create.html',
                  {'form': form})


def band_update(request, band_id):
    band = Band.objects.get(id=band_id)

    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)  # on pré-rempli le formulaire avec le groupe existant
        if form.is_valid():
            # mettre à jour le groupe exietant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return HttpResponseRedirect(reverse('band-detail', kwargs={'band_id': band.id}))
    else:
        form = BandForm(instance=band)

    return render(request,
                  'listings/band_update.html',
                  {'form': form})


def band_delete(request, band_id):
    band = Band.objects.get(id=band_id)

    if request.method == 'POST':
        # supprimer le groupe de la BDD
        band.delete()
        # rediriger vers la liste des groupes
        return HttpResponseRedirect(reverse('band-list'))

    return render(request,
                  'listings/band_delete.html',
                  {'band': band})


def about(request):
    return render(request, 'listings/about.html')


def listings_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/listings_list.html',
                  context={'listings': listings})


def listings_detail(request, listing_id):
    listings = Listing.objects.get(id=listing_id)
    return render(request, 'listings/listings_detail.html',
                  {'listings': listings})


def listings_create(request):
    if request.method == 'POST':
        form = ListingsForm(request.POST)
        if form.is_valid():
            # Créer une nouvelle "Listing" et la sauvegarder dans la database
            listings = form.save()
            # Redirige vers la page de détail du groupe que nous venons de créer
            # On peut fournir les arguements du motif url comme arguments à la fonction de redirection
            return HttpResponseRedirect(reverse('listings-detail', kwargs={'listing_id': listings.id}))
    else:
        form = ListingsForm()

    return render(request, 'listings/listings_create.html',
                  {'form': form})


def listings_update(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.method == 'POST':
        form = ListingsForm(request.POST, instance=listing)  # on pré-rempli le formulaire avec le groupe existant
        if form.is_valid():
            # mettre à jour le groupe exietant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return HttpResponseRedirect(reverse('listings-detail', kwargs={'listing_id': listing.id}))
    else:
        form = ListingsForm(instance=listing)

    return render(request,
                  'listings/listings_update.html',
                  {'form': form})


def listings_delete(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.method == 'POST':
        # supprimer le groupe de la BDD
        listing.delete()
        # rediriger vers la liste des groupes
        return redirect('listings_list')

    return render(request,
                  'listings/listings_delete.html',
                  {'listing': listing})


def contact(request):
      # ajoutez ces instructions d'impression afin que nous puissions jeter un coup d'oeil à « request.method » et à « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)

    if request.method == 'POST':
    # créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
                message=form.cleaned_data["message"],
                from_email=form.cleaned_data["email"],
                recipient_list=["admin@merchex.xyz"]
            )
            return redirect('email-sent')

    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()

    return render(request, 'listings/contact.html',
                  {'form': form})
