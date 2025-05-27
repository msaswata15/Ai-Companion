import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'

const app = express()
app.use(cors())
app.use(bodyParser.json())

app.post('/api/resume', (req, res) => {
    const { jobDesc } = req.body
    if (!jobDesc) return res.status(400).json({ error: 'Missing jobDesc' })
    res.json({
        resume: `Resume for job/scholarship:\n\n${jobDesc.slice(0, 200)}\n\nSkills:\n- Communication\n- Problem Solving\n- Teamwork\n\nEducation:\n- Bachelor of Technology\n\nExperience:\n- Internship at Example Corp`,
        coverLetter: `Dear Hiring Manager,\n\nI am excited to apply for this opportunity. My background in technology and my passion for learning make me a strong fit for this role.\n\n${jobDesc.slice(0, 120)}\n\nSincerely,\nStudent`
    })
})

app.post('/api/interview', (req, res) => {
    const { answer } = req.body
    if (!answer) return res.status(400).json({ error: 'Missing answer' })
    try {
        // eslint-disable-next-line no-new-func
        const fn = new Function('return ' + answer)
        const userFunc = fn()
        let feedback
        if (typeof userFunc === 'function') {
            const test = userFunc('hello')
            if (test === 'olleh') {
                feedback = '✅ Correct! Your function reverses a string.'
            } else {
                feedback = '⚠️ Your function does not return the correct result for "hello".'
            }
        } else {
            feedback = '⚠️ Please define a function.'
        }
        res.json({ feedback })
    } catch (e) {
        res.json({ feedback: '❌ Error in code: ' + e.message })
    }
})

const CHEAT_SHEETS = {
    'binary search': `Binary Search:
- Used to find an element in a sorted array in O(log n) time.
- Example (JavaScript):
function binarySearch(arr, target) {
  let l = 0, r = arr.length - 1;
  while (l <= r) {
    const m = Math.floor((l + r) / 2);
    if (arr[m] === target) return m;
    if (arr[m] < target) l = m + 1;
    else r = m - 1;
  }
  return -1;
}`,
    'linked list': `Linked List:
- Data structure of nodes, each with a value and pointer to next.
- Example (JavaScript):
class Node {
  constructor(val) {
    this.val = val;
    this.next = null;
  }
}`,
    'sorting': `Sorting Algorithms:
- Bubble Sort, Merge Sort, Quick Sort, etc.
- Example (Bubble Sort):
function bubbleSort(arr) {
  for (let i = 0; i < arr.length; i++)
    for (let j = 0; j < arr.length - i - 1; j++)
      if (arr[j] > arr[j+1]) [arr[j], arr[j+1]] = [arr[j+1], arr[j]];
  return arr;
}`
}

app.post('/api/cheatsheet', (req, res) => {
    const { topic } = req.body
    if (!topic) return res.status(400).json({ error: 'Missing topic' })
    const key = topic.trim().toLowerCase()
    res.json({
        cheatSheet: CHEAT_SHEETS[key] || `Cheat sheet for "${topic}":\n- Key concept 1\n- Key concept 2\n- Example code...`
    })
})

const PORT = process.env.PORT || 4000
app.listen(PORT, () => {
    console.log(`Backend running on port ${PORT}`)
})
