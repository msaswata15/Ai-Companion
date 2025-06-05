// API endpoints
const API = {
  UPLOAD_RESUME: '/api/career/upload-resume',
  GET_RECOMMENDATIONS: '/api/career/recommendations',
  SEARCH_JOBS: '/api/career/search-jobs',
  GENERATE_CHEAT_SHEET: '/api/career/cheat-sheet'
};

// Handle resume upload
async function uploadResume(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(API.UPLOAD_RESUME, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Upload failed');
    
    const data = await response.json();
    return data.resume_text;
  } catch (error) {
    console.error('Resume upload error:', error);
    throw error;
  }
}

// Search jobs
async function searchJobs(keywords, location = '') {
  const formData = new FormData();
  formData.append('keywords', keywords);
  if (location) formData.append('location', location);

  try {
    const response = await fetch(API.SEARCH_JOBS, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Job search failed');
    
    return await response.json();
  } catch (error) {
    console.error('Job search error:', error);
    throw error;
  }
}

// Generate cheat sheet
async function generateCheatSheet(topic, context = '') {
  const formData = new FormData();
  formData.append('topic', topic);
  if (context) formData.append('context', context);

  try {
    const response = await fetch(API.GENERATE_CHEAT_SHEET, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Cheat sheet generation failed');
    
    const data = await response.json();
    return data.content;
  } catch (error) {
    console.error('Cheat sheet error:', error);
    throw error;
  }
}

// Display job results
function displayJobs(jobs) {
  const resultsDiv = document.getElementById('jobResults');
  resultsDiv.innerHTML = '';

  jobs.forEach(job => {
    const jobCard = document.createElement('div');
    jobCard.className = 'card';
    jobCard.innerHTML = `
      <h3>${job.title}</h3>
      <p><strong>${job.company}</strong> - ${job.location}</p>
      <p>${job.description.substring(0, 200)}...</p>
      <a href="${job.url}" target="_blank" class="btn">View Job</a>
    `;
    resultsDiv.appendChild(jobCard);
  });
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
  const resumeUpload = document.getElementById('resumeUpload');
  const jobSearchForm = document.getElementById('jobSearchForm');
  const cheatSheetForm = document.getElementById('cheatSheetForm');

  if (resumeUpload) {
    resumeUpload.addEventListener('change', async (e) => {
      try {
        const file = e.target.files[0];
        const resumeText = await uploadResume(file);
        document.getElementById('resumeText').textContent = resumeText;
      } catch (error) {
        alert('Resume upload failed: ' + error.message);
      }
    });
  }

  if (jobSearchForm) {
    jobSearchForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const keywords = document.getElementById('keywords').value;
      const location = document.getElementById('location').value;
      
      try {
        const jobs = await searchJobs(keywords, location);
        displayJobs(jobs);
      } catch (error) {
        alert('Job search failed: ' + error.message);
      }
    });
  }

  if (cheatSheetForm) {
    cheatSheetForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const topic = document.getElementById('topic').value;
      
      try {
        const content = await generateCheatSheet(topic);
        document.getElementById('cheatSheetContent').innerHTML = marked.parse(content);
      } catch (error) {
        alert('Cheat sheet generation failed: ' + error.message);
      }
    });
  }
});