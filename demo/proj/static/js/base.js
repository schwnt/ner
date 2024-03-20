function filterAndNormalizeEntities(text, ents) {
  const entTable = {};

  for (const [label, start, end] of ents) {
    if (!["MISC"].includes(label)) {
      let textSubstring = text.substring(start, end).trim(); // Normalize the text
      textSubstring = textSubstring.replace(/[.,\s]+$/g, ''); // Remove trailing punctuation and spaces

      if (!(label in entTable)) {
        entTable[label] = {}; 
      }
      entTable[label][textSubstring] = true; 
    }
  }

  for (const label in entTable) {
    entTable[label] = Object.keys(entTable[label]);
  }
  return entTable;
}

function populateTable(entTable) {
  const tableBody = document.querySelector("#resultTable tbody");
  tableBody.innerHTML = ''; // Clear existing rows

  for (const label in entTable) {
    const row = tableBody.insertRow();
    const column1 = row.insertCell(0);
    const column2 = row.insertCell(1);

    column1.textContent = label;
    
    const entTexts = [];
    const rectanglesDiv = document.createElement('div');
    rectanglesDiv.classList.add('label-rectangles');

    entTable[label].forEach(entText => {
      const rectangle = document.createElement('div');
      rectangle.style.backgroundColor = getLabelColor(label); 
      rectangle.textContent = entText; 
      rectanglesDiv.appendChild(rectangle);

      entTexts.push(entText); 
    });
    column2.appendChild(rectanglesDiv);

    const copyButton = document.createElement('button');
    copyButton.textContent = 'Copy';
    copyButton.classList.add('copy-button'); 
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');
    buttonContainer.appendChild(copyButton);
    copyButton.addEventListener('click', function(){
      if (navigator.clipboard) {
        navigator.clipboard.writeText(entTexts.join(', '));
      }
    });

    column2.appendChild(buttonContainer); 
  }
}

function buildHighlightedText(text, entityPositions) {
  let highlightedText = '';
  let lastIndex = 0;

  for (const [start, end] of entityPositions) {
    highlightedText += text.substring(lastIndex, start);
    highlightedText += `<span class="highlighted-entity">${text.substring(start, end)}</span>`;
    lastIndex = end;
  }

  highlightedText += text.substring(lastIndex); 
  return highlightedText;
}


function handleSubmit() {
  const url = document.getElementById('urlInput').value;
  const selectedModel = document.getElementById('modelDropdown').value; // Get the selected model
  const queryParams = `?u=${url}&m=${selectedModel}`;
  
  fetch('/data/' + queryParams)
  .then(response => response.json())
    .then(data => {
      const text = data.text;
      const ents = data.ents.filter(ent => ent[0] !== "MISC");
      const entTable = filterAndNormalizeEntities(text, ents);
      populateTable(entTable); 

      const entityPositions = ents.map(ent => [ent[1], ent[2]]);
      document.getElementById('textDisplay').innerHTML = buildHighlightedText(text, entityPositions);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById('submitButton');
  button.addEventListener('click', handleSubmit);
  
  const showTextButton = document.getElementById('showTextButton');
  showTextButton.textContent = 'Show Text';
  const textDisplayContainer = document.getElementById('textDisplayContainer');
  let isTextDisplayVisible = false;
  textDisplayContainer.style.display = 'none';
  showTextButton.classList.remove('show-button');
  showTextButton.classList.add('hide-button');
  
  showTextButton.addEventListener('click', function() {
    isTextDisplayVisible = !isTextDisplayVisible;
    textDisplayContainer.style.display = isTextDisplayVisible ? 'block' : 'none';
    
    if (isTextDisplayVisible) {
      showTextButton.classList.remove('hide-button');
      showTextButton.classList.add('show-button');
    } else {
      showTextButton.classList.remove('show-button');
      showTextButton.classList.add('hide-button');
    }
  });
});

function getLabelColor(label) {
  return 'green'; // Default color
  switch (label) {
    case 'PER':
      return 'red';
      case 'LOC':
        return 'blue';
    case 'ORG':
      return 'green';
      default:
        return 'gray';
      }
}