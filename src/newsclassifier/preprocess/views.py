from collections import OrderedDict

from hinditokenizer import *

from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin, DetailView

from .forms import *


class TokenizeView(SingleObjectMixin, ListView):

    template_name = 'preprocess/tokenize.html'
    form_class = TokenizeForm

    def get(self, request, *args, **kwargs):
        form_obj = self.form_class(request.GET or None)
        no_hyphen_tokens, sentences, tokens, unique_tokens = [None] * 4
        hyphenTokenPresent = False
        # for finding unique tokens
        token_list = []
        unique_tokens_map = OrderedDict()

        if form_obj.is_valid():
            text = form_obj.cleaned_data.get('text')
            sentences = tokenize_sent(text)
            tokens = tokenize(text)

            no_hyphen_tokens, hyphenTokenPresent = remove_hyphenated_tokens(tokens, verbose_mode=True)

            # by default unique operation will be applied
            # on whole token set. However if any hyphenated token
            # is present, then it should be on `no_hyphen_tokens`
            if not hyphenTokenPresent:
                no_hyphen_tokens = None
                token_list = tokens
            else:
                token_list = no_hyphen_tokens

            # not using `set` to find unique tokens, since it does
            # not preserves the order
            for token in token_list:
                unique_tokens_map.setdefault(token, 0)
                unique_tokens_map[token]+=1

        return render(request, self.template_name, {
            'form': form_obj,
            'no_hyphen_tokens': no_hyphen_tokens,
            'sentences': sentences,
            'tokens': tokens,
            'unique_tokens': unique_tokens_map,
        })
