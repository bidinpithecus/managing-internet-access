function createPCContainer(pc) {
    // Cria o contêiner principal
    const container = document.createElement('div');
    container.className = 'pc-container';

    // Cria o contêiner do ícone
    const iconDiv = document.createElement('div');
    iconDiv.className = 'icon';

    const img = document.createElement('img');
    img.src = 'pc-icon.png';
    img.alt = 'PC Icon';
    img.className = 'pc-icon';

    iconDiv.appendChild(img);

    // Cria o contêiner de status
    const statusDiv = document.createElement('div');
    statusDiv.className = 'dashboard-status';

    const idP = document.createElement('p');
    idP.textContent = `Id: ${pc.id}`;

    const statusP = document.createElement('p');
    statusP.textContent = `Status: ${pc.status}`;

    statusDiv.appendChild(idP);
    statusDiv.appendChild(statusP);

    // Cria o contêiner dos botões
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'pc-btn-container';

    const button1 = document.createElement('button');
    button1.className = 'pc-button';
    button1.textContent = 'Agendar bloqueio';

    const button2 = document.createElement('button');
    button2.className = 'pc-button';
    button2.textContent = 'Desbloquear';

    buttonContainer.appendChild(button1);
    buttonContainer.appendChild(button2);

    // Junta tudo no contêiner principal
    container.appendChild(iconDiv);
    container.appendChild(statusDiv);
    container.appendChild(buttonContainer);

    return container;
}

// function addPCContainersToDocument(pcs, containerElement) {
//     pcs.forEach(pc => {
//         const pcContainer = createPCContainer(pc);
//         containerElement.appendChild(pcContainer);
//     });
// }

// const pcs = Array.from({ length: 24 }, (v, k) => ({
//     id: k + 1,
//     status: k % 2 === 0 ? 'Online' : 'Offline'
// }));

// const containerElement = document.getElementById('pc-containers');
// addPCContainersToDocument(pcs, containerElement);

document.addEventListener('DOMContentLoaded', () => {
    const gridItems = document.querySelectorAll('.grid-item');
    const toggleSelectButton = document.getElementById('toggle-select');
    const popup = document.getElementById('popup');
    const popupContent = document.querySelector('.popup-content');
    const closeBtn = document.querySelector('.close');

    // Event listener for grid items click
    gridItems.forEach(item => {
        item.addEventListener('click', () => {
            if (item.classList.contains('green') || item.classList.contains('red')) {
                item.classList.toggle('selected');
            }
        });

        // Event listener for grid items double click
        item.addEventListener('dblclick', () => {
            showPopup();
        });
    });

    // Event listener for toggle select button click
    toggleSelectButton.addEventListener('click', () => {
        const isSelected = toggleSelectButton.dataset.selected === 'true';

        if (!isSelected) {
            gridItems.forEach(item => {
                if (item.classList.contains('green') || item.classList.contains('red')) {
                    item.classList.add('selected');
                }
            });
            toggleSelectButton.textContent = 'Deselecionar';
            toggleSelectButton.dataset.selected = 'true';
        } else {
            gridItems.forEach(item => {
                item.classList.remove('selected');
            });
            toggleSelectButton.textContent = 'Selecionar';
            toggleSelectButton.dataset.selected = 'false';
            hidePopup(); // Hide popup if deselecting all
        }
    });

    function showPopup() {
        // Example content for demonstration
        const rowData = [
            { port: 'Port 1', status: 'Active', lastUpdate: '2024-07-01 10:00:00' },
            { port: 'Port 2', status: 'Inactive', lastUpdate: '2024-07-01 09:30:00' }
        ];

        // Clear previous content
        popupContent.querySelector('tbody').innerHTML = '';

        // Build table rows with example data
        rowData.forEach(data => {
            const row = `
                <tr>
                    <td>${data.port}</td>
                    <td>${data.status}</td>
                    <td>${data.lastUpdate}</td>
                </tr>
            `;
            popupContent.querySelector('tbody').insertAdjacentHTML('beforeend', row);
        });

        // Show the popup
        popup.style.display = 'block';
    }

    // Function to hide the popup
    function hidePopup() {
        popup.style.display = 'none';
    }

    // Close button click event
    closeBtn.addEventListener('click', function() {
        hidePopup();
    });
});

