const API_URL = 'http://127.0.0.1:8000/api';

let currentCampaignId = null;

async function loadCampaigns() {
    const res = await fetch(`${API_URL}/campaigns`);
    const campaigns = await res.json();
    const tbody = document.querySelector('#campaignsTable tbody');
    tbody.innerHTML = '';
    
    campaigns.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${c.id}</td>
            <td>${c.name}</td>
            <td>${c.geo}</td>
            <td>${c.offer_id}</td>
            <td>${c.keitaro_id}</td>
            <td>
                <button class="btn" onclick="selectCampaign(${c.id}, '${c.name}')">Офферы</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function createCampaign() {
    const name = document.getElementById('campaignName').value;
    const geo = document.getElementById('campaignGeo').value;
    const offer_id = parseInt(document.getElementById('campaignOfferId').value);
    
    const status = document.getElementById('createStatus');
    status.textContent = 'Создание...';

    try {
        const res = await fetch(`${API_URL}/campaigns`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, geo, offer_id})
        });
        
        if (res.ok) {
            status.textContent = 'Кампания создана!';
            document.getElementById('campaignName').value = '';
            document.getElementById('campaignGeo').value = '';
            document.getElementById('campaignOfferId').value = '';
            loadCampaigns();
        } else {
            const err = await res.json();
            status.textContent = 'Ошибка: ' + JSON.stringify(err.detail);
        }
    } catch (e) {
        status.textContent = 'Ошибка: ' + e.message;
    }
}

async function selectCampaign(id, name) {
    currentCampaignId = id;
    document.getElementById('currentCampaignName').textContent = `(${name})`;
    document.getElementById('offersSection').style.display = 'block';
    await loadOffers();
}

async function loadOffers() {
    if (!currentCampaignId) return;
    const res = await fetch(`${API_URL}/campaigns/${currentCampaignId}/offers`);
    const offers = await res.json();
    const list = document.getElementById('offersList');
    list.innerHTML = '';
    
    if (offers.length === 0) {
        list.innerHTML = '<li>Нет офферов</li>';
        return;
    }
    
    offers.forEach(o => {
        const li = document.createElement('li');
        li.innerHTML = `
            Offer ID: ${o.offer_id} (Stream: ${o.stream_name}) 
            <button class="btn btn-danger" onclick="removeOffer(${o.offer_id})">Удалить</button>
        `;
        list.appendChild(li);
    });
}

async function addOffer() {
    if (!currentCampaignId) return;
    const offerId = parseInt(document.getElementById('newOfferId').value);
    
    try {
        const res = await fetch(`${API_URL}/campaigns/${currentCampaignId}/offers`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({offer_id: offerId})
        });
        
        if (res.ok) {
            document.getElementById('newOfferId').value = '';
            await loadOffers();
        } else {
            const err = await res.json();
            alert('Ошибка: ' + JSON.stringify(err.detail));
        }
    } catch (e) {
        alert('Ошибка: ' + e.message);
    }
}

async function removeOffer(offerId) {
    if (!currentCampaignId) return;
    if (!confirm('Удалить оффер ' + offerId + '?')) return;

    try {
        const res = await fetch(`${API_URL}/campaigns/${currentCampaignId}/offers/${offerId}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            await loadOffers();
        } else {
            const err = await res.json();
            alert('Ошибка: ' + JSON.stringify(err.detail));
        }
    } catch (e) {
        alert('Ошибка: ' + e.message);
    }
}

document.addEventListener('DOMContentLoaded', loadCampaigns);