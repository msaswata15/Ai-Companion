import { useState } from 'react'
import './App.css'

function ResumeGenerator() {
    const [jobDesc, setJobDesc] = useState('')
    const [resume, setResume] = useState('')
    const [coverLetter, setCoverLetter] = useState('')
    const [loading, setLoading] = useState(false)

    const handleGenerate = async () => {
        setLoading(true)
        // Simulate async API call
        await new Promise(r => setTimeout(r, 1200))
        setResume(
            `Resume for job/scholarship:\n\n${jobDesc.slice(0, 200)}\n\nSkills:\n- Communication\n- Problem Solving\n- Teamwork\n\nEducation:\n- Bachelor of Technology\n\nExperience:\n- Internship at Example Corp`
        )
        setCoverLetter(
            `Dear Hiring Manager,\n\nI am excited to apply for this opportunity. My background in technology and my passion for learning make me a strong fit for this role.\n\n${jobDesc.slice(0, 120)}\n\nSincerely,\nStudent`
        )
        setLoading(false)
    }

    return (
        <div>
            <h2>Resume & Cover Letter Generator</h2>
            <textarea
                rows={5}
                placeholder="Paste job/scholarship description here..."
                value={jobDesc}
                onChange={e => setJobDesc(e.target.value)}
                style={{ width: '100%' }}
            />
            <br />
            <button onClick={handleGenerate} disabled={!jobDesc.trim() || loading}>
                {loading ? 'Generating...' : 'Generate'}
            </button>
            {resume && (
                <>
                    <h3>Resume</h3>
                    <pre>{resume}</pre>
                </>
            )}
            {coverLetter && (
                <>
                    <h3>Cover Letter</h3>
                    <pre>{coverLetter}</pre>
                </>
            )}
        </div>
    )
}

function MockInterview() {
    const [question, setQuestion] = useState('Implement a function to reverse a string.')
    const [answer, setAnswer] = useState('')
    const [feedback, setFeedback] = useState('')
    const [hint, setHint] = useState('')
    const [loading, setLoading] = useState(false)

    const handleEvaluate = async () => {
        setLoading(true)
        setFeedback('')
        // Simulate code evaluation
        await new Promise(r => setTimeout(r, 1000))
        try {
            // Very basic check for correct logic
            // eslint-disable-next-line no-new-func
            const fn = new Function('return ' + answer)
            const userFunc = fn()
            if (typeof userFunc === 'function') {
                const test = userFunc('hello')
                if (test === 'olleh') {
                    setFeedback('✅ Correct! Your function reverses a string.')
                } else {
                    setFeedback('⚠️ Your function does not return the correct result for "hello".')
                }
            } else {
                setFeedback('⚠️ Please define a function.')
            }
        } catch (e) {
            setFeedback('❌ Error in code: ' + e.message)
        }
        setLoading(false)
    }

    const handleHint = () => {
        setHint('Hint: Convert the string to an array, use reverse(), then join back.')
    }

    return (
        <div>
            <h2>Mock Algorithmic Interview</h2>
            <div>
                <strong>Question:</strong>
                <div>{question}</div>
            </div>
            <textarea
                rows={5}
                placeholder={`e.g.\nfunction reverseString(str) {\n  return str.split('').reverse().join('');\n}`}
                value={answer}
                onChange={e => setAnswer(e.target.value)}
                style={{ width: '100%' }}
            />
            <br />
            <button onClick={handleEvaluate} disabled={!answer.trim() || loading}>
                {loading ? 'Evaluating...' : 'Evaluate'}
            </button>
            <button onClick={handleHint} style={{ marginLeft: 8 }}>Hint</button>
            {feedback && (
                <div style={{ marginTop: 12 }}>
                    <strong>Feedback:</strong>
                    <div>{feedback}</div>
                </div>
            )}
            {hint && (
                <div style={{ marginTop: 8 }}>
                    <strong>Hint:</strong>
                    <div>{hint}</div>
                </div>
            )}
        </div>
    )
}

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

function CheatSheetBuilder() {
    const [topic, setTopic] = useState('')
    const [cheatSheet, setCheatSheet] = useState('')
    const [loading, setLoading] = useState(false)

    const handleBuild = async () => {
        setLoading(true)
        await new Promise(r => setTimeout(r, 800))
        const key = topic.trim().toLowerCase()
        setCheatSheet(CHEAT_SHEETS[key] || `Cheat sheet for "${topic}":\n- Key concept 1\n- Key concept 2\n- Example code...`)
        setLoading(false)
    }

    return (
        <div>
            <h2>Algorithm Cheat Sheet Builder</h2>
            <input
                type="text"
                placeholder="Enter algorithm/topic (e.g. Binary Search)..."
                value={topic}
                onChange={e => setTopic(e.target.value)}
                style={{ width: '60%' }}
            />
            <button onClick={handleBuild} disabled={!topic.trim() || loading} style={{ marginLeft: 8 }}>
                {loading ? 'Building...' : 'Build'}
            </button>
            {cheatSheet && (
                <pre style={{ textAlign: 'left', marginTop: 16, whiteSpace: 'pre-wrap' }}>{cheatSheet}</pre>
            )}
        </div>
    )
}

function App() {
    const [tab, setTab] = useState('resume')

    return (
        <div>
            <h1>AI Career Companion</h1>
            <div style={{ marginBottom: 24 }}>
                <button onClick={() => setTab('resume')} disabled={tab === 'resume'}>Resume Generator</button>
                <button onClick={() => setTab('interview')} disabled={tab === 'interview'} style={{ marginLeft: 8 }}>Mock Interview</button>
                <button onClick={() => setTab('cheatsheet')} disabled={tab === 'cheatsheet'} style={{ marginLeft: 8 }}>Cheat Sheet Builder</button>
            </div>
            <div className="card">
                {tab === 'resume' && <ResumeGenerator />}
                {tab === 'interview' && <MockInterview />}
                {tab === 'cheatsheet' && <CheatSheetBuilder />}
            </div>
        </div>
    )
}

export default App
