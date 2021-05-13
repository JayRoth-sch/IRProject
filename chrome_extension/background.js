function resetDefaultSuggestion() {
    chrome.omnibox.setDefaultSuggestion({
      description: "Try these more fair results! Alternatively, hit enter to see Google's results"
    });
  }
  
  resetDefaultSuggestion();
  
  let timeout = null;
  chrome.omnibox.onInputChanged.addListener(function(text, suggest) {
    chrome.omnibox.setDefaultSuggestion({
        description: "Loading fair results..."
      });
    clearTimeout(timeout);
    timeout = setTimeout(function () {
        x = new XMLHttpRequest();
        x.onreadystatechange = function() {
            if (x.readyState === 4) {
                resetDefaultSuggestion();
                response = JSON.parse(x.responseText);
                suggestions = [];
                topfive = response.fair_top_5.replace('[', '').replace(']','').replaceAll('\'', '').split(", ");
                topfive.forEach(function(suggestion) {
                    suggestions.push({content: suggestion, description: suggestion});
                });
                suggest(suggestions);
            }
        }
        x.open('GET', 'https://cors-anywhere.herokuapp.com/http://www.jayrothenberger.com/test/?query='+text);
        x.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        x.send();
    }, 1000);
    
  });
  
  chrome.omnibox.onInputCancelled.addListener(function() {
    resetDefaultSuggestion();
  });
  
  function navigate(url) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.update(tabs[0].id, {url: url});
    });
  }
  
  chrome.omnibox.onInputEntered.addListener(function(text) {
    if (text.substr(0, 4) == "http") {
        navigate(text)
    }
    else {
        navigate("https://www.google.com/search?q=" + text);
    }
    
  });