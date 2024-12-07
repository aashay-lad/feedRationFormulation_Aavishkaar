// static/js/cost_estimation.js
document.getElementById('cost-estimation-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const cornPrice = document.getElementById('corn-price').value;
    const soyPrice = document.getElementById('soy-price').value;
    const wheatPrice = document.getElementById('wheat-price').value;
    const alfalfaPrice = document.getElementById('alfalfa-price').value;

    fetch('/calculate-cost', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cornPrice, soyPrice, wheatPrice, alfalfaPrice })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('total-cost').innerText = `Total Cost: Rs.${data.total_cost}`;
        document.getElementById('cost-result').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});
