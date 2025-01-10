document.getElementById('poissonForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const lambda = parseFloat(document.getElementById('lambda').value);
    const x = parseInt(document.getElementById('x').value);

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ lambda, x }),
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById('result').innerHTML = `<p class="error">Error: ${data.error}</p>`;
        } else {
            const pExact = data.probability;
            const pLess = calculateCumulativeProbability(lambda, x - 1);
            const pLessEqual = calculateCumulativeProbability(lambda, x);
            const pGreater = (1 - pLessEqual).toFixed(6);
            const pGreaterEqual = (1 - pLess).toFixed(6);

            document.getElementById('result').innerHTML = `
                <div class="result-container">
                    <h2>Poisson Distribution Results</h2>
                    <h3>Output P(X = ${x})</h3>
                    <p><strong>Rumus:</strong> P(X = x) = (e<sup>-λ</sup> * λ<sup>x</sup>) / x!</p>
                    <p><strong>Langkah Perhitungan:</strong></p>
                    <p>P(X = ${x}) = (e<sup>-${lambda}</sup> * ${lambda}<sup>${x}</sup>) / ${x}!<br>
                    P(X = ${x}) = (${Math.exp(-lambda).toFixed(6)} * ${Math.pow(lambda, x).toFixed(6)}) / ${factorial(x)}<br>
                    P(X = ${x}) = ${pExact}</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Keterangan</th>
                                <th>Nilai</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>P(X = ${x})</td><td>${pExact}</td></tr>
                            <tr><td>P(X < ${x})</td><td>${pLess}</td></tr>
                            <tr><td>P(X ≤ ${x})</td><td>${pLessEqual}</td></tr>
                            <tr><td>P(X > ${x})</td><td>${pGreater}</td></tr>
                            <tr><td>P(X ≥ ${x})</td><td>${pGreaterEqual}</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});

function factorial(n) {
    return n === 0 ? 1 : n * factorial(n - 1);
}

function calculateCumulativeProbability(lambda, maxX) {
    let cumulativeProbability = 0;
    for (let i = 0; i <= maxX; i++) {
        cumulativeProbability += (Math.exp(-lambda) * Math.pow(lambda, i)) / factorial(i);
    }
    return cumulativeProbability.toFixed(6);
}
