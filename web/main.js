import { streamGemini } from './gemini-api.js';

let form = document.getElementById('ipr-form');
let fileUpload = document.getElementById('excel-upload');
let websiteInput = document.querySelector('input[name="website"]');
let resultText = document.getElementById('result-text');

form.onsubmit = async (ev) => {
  ev.preventDefault();
  resultText.textContent = 'Analyzing...';

  try {
    // Read the uploaded Excel file
    let file = fileUpload.files[0];
    if (!file) {
      throw new Error("Please upload an Excel file.");
    }

    let data = await readExcel(file);
    let website = websiteInput.value.trim();

    if (!website) {
      throw new Error("Please enter a website or keyword.");
    }

    // Prepare the prompt for Gemini
    let prompt = `Analyze the following website/keyword for Disney IPR violations based on the provided data:\n\nWebsite/Keyword: ${website}\n\nExcel Data:\n${JSON.stringify(data, null, 2)}`;

    // Call the Gemini API
    let stream = streamGemini({
      model: 'gemini-1.5-flash', // or gemini-1.5-pro
      contents: [{ type: "text", text: prompt }],
    });

    // Display the results
    let buffer = [];
    let md = new markdownit();
    for await (let chunk of stream) {
      buffer.push(chunk);
      resultText.innerHTML = md.render(buffer.join(''));
    }
  } catch (e) {
    resultText.innerHTML = `<span style="color: red;">Error: ${e.message}</span>`;
  }
};

// Function to read Excel file
async function readExcel(file) {
  return new Promise((resolve, reject) => {
    let reader = new FileReader();
    reader.onload = (e) => {
      let data = new Uint8Array(e.target.result);
      let workbook = XLSX.read(data, { type: 'array' });
      let sheetName = workbook.SheetNames[0];
      let sheet = workbook.Sheets[sheetName];
      let json = XLSX.utils.sheet_to_json(sheet);
      resolve(json);
    };
    reader.onerror = (e) => reject(new Error("Failed to read the Excel file."));
    reader.readAsArrayBuffer(file);
  });
}