async function analyze() {

    const resumeText = document.getElementById("resume_text").value;
    const jobDescription = document.getElementById("job_description").value;

    const response = await fetch("/match", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription
        })
    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <h3>ATS Score: ${data.final_ats_score}</h3>
        <p><strong>Semantic Score:</strong> ${data.semantic_score}</p>
        <p><strong>Skill Match Score:</strong> ${data.skill_match_score}</p>
        <p><strong>Matched Skills:</strong> ${data.matched_skills}</p>
        <p><strong>Missing Skills:</strong> ${data.missing_skills}</p>
    `;
}
