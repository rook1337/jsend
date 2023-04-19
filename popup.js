// Define the regex pattern
const REGEX_PATTERN = /(?:"|')(((?:[a-zA-Z]{1,10}:\/\/|\/\/)[^"'\/]{1,}\.[a-zA-Z]{2,}[^"'\/]{0,})|((?:\/|\.\.\/|\.\/)[^"'<>;,| *()\\[\]][^"'<>;,|()]{1,})|([a-zA-Z0-9_\-\/]{1,}\/[a-zA-Z0-9_\-\/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[?|#][^"'\\]{0,}|))|([a-zA-Z0-9_\-\/]{1,}\/[a-zA-Z0-9_\-\/]{3,}(?:[?|#][^"'\\]{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[?|#][^"'\\]{0,}|)))(?:"|')/g;

// Define the function that fetches endpoints from the current tab loaded page
function fetchEndpoints() {
  // Get the current tab
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) 
{
    // Get the HTML content of the current tab
    chrome.tabs.executeScript(
      tabs[0].id,
      { code: 'document.documentElement.outerHTML' },
      function (results) {
        // Extract the endpoints from the HTML content using the regex pattern
        const htmlContent = results[0];
        const endpoints = htmlContent.match(REGEX_PATTERN);
        // Display the endpoints in a new tab
        chrome.tabs.create({ url: 'data:text/html;charset=utf-8,' + encodeURIComponent(endpoints.join('<br>')) });
      }
    );
  });
}

// Add an event listener to the button that triggers the endpoint fetching functionality
document.getElementById('fetchButton').addEventListener('click', 
fetchEndpoints);

