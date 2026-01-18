// Функция для заполнения таблицы фильмами
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            // Получаем тело таблицы по id и очищаем его
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            // Пробегаемся по массиву фильмов
            for(let i = 0; i < films.length; i++) {
                // Создаем строку
                let tr = document.createElement('tr');
                
                // Создаем ячейки
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');
                
                // Заполняем данными из массива фильмов
                // Если русское и оригинальное название совпадают, оригинальное не выводим
                tdTitle.innerHTML = films[i].title === films[i].title_ru ? '' : films[i].title;
                tdTitleRus.innerHTML = films[i].title_ru;
                tdYear.innerHTML = films[i].year;
                
                // Создаем кнопки редактирования и удаления
                let editButton = document.createElement('button');
                editButton.innerHTML = 'редактировать';
                editButton.onclick = function() {
                    loadFilmForEdit(i);
                };
                editButton.style.marginRight = '10px';
                editButton.style.padding = '5px 10px';
                editButton.style.background = '#FF9800';
                editButton.style.color = 'white';
                editButton.style.border = 'none';
                editButton.style.borderRadius = '3px';
                editButton.style.cursor = 'pointer';
                
                let delButton = document.createElement('button');
                delButton.innerHTML = 'удалить';
                delButton.onclick = function() {
                    deleteFilm(i, films[i].title_ru);
                };
                delButton.style.padding = '5px 10px';
                delButton.style.background = '#f44336';
                delButton.style.color = 'white';
                delButton.style.border = 'none';
                delButton.style.borderRadius = '3px';
                delButton.style.cursor = 'pointer';
                
                // Добавляем кнопки в ячейку действий
                tdActions.appendChild(editButton);
                tdActions.appendChild(delButton);
                
                // Добавляем ячейки в строку
                tr.appendChild(tdTitleRus);
                tr.appendChild(tdTitle);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);
                
                // Добавляем строку в таблицу
                tbody.appendChild(tr);
            }
            
            // Обновляем статистику
            updateStats();
        })
        .catch(function (error) {
            console.error('Ошибка загрузки фильмов:', error);
            document.getElementById('film-list').innerHTML = 
                '<tr><td colspan="4" style="color: red; text-align: center; padding: 20px;">Ошибка загрузки данных</td></tr>';
        });
}

// Функция загрузки фильма для редактирования
function loadFilmForEdit(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(response) {
            return response.json();
        })
        .then(function(film) {
            // Заполняем форму редактирования
            document.getElementById('editId').value = id;
            document.getElementById('editTitle').value = film.title;
            document.getElementById('editTitleRu').value = film.title_ru;
            document.getElementById('editYear').value = film.year;
            document.getElementById('editDescription').value = film.description;
            
            // Показываем сообщение
            const output = document.getElementById('output');
            output.innerHTML = `<h3>Редактирование фильма #${id}: "${film.title_ru}"</h3>
                              <p>Заполните форму выше и нажмите "Обновить фильм"</p>`;
        })
        .catch(function(error) {
            console.error('Ошибка:', error);
            alert('Ошибка при загрузке данных фильма');
        });
}

// Функция удаления фильма (с улучшениями из методички)
function deleteFilm(id, title) {
    // Добавляем подтверждение с именем фильма
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(function(response) {
        if (response.status === 204) {
            // Показываем сообщение об успешном удалении
            const output = document.getElementById('output');
            output.innerHTML = `<h3>Фильм "${title}" успешно удален!</h3>`;
            
            // Перезагружаем таблицу после удаления
            setTimeout(fillFilmList, 500);
        } else {
            response.json().then(function(error) {
                alert(`Ошибка при удалении фильма: ${error.error || 'Неизвестная ошибка'}`);
            });
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении фильма. Проверьте подключение к серверу.');
    });
}

// Функция для показа формы добавления
function addFilm() {
    // Создаем форму добавления динамически
    const output = document.getElementById('output');
    output.innerHTML = `
        <h3>Добавление нового фильма</h3>
        <div style="background: #f5f5f5; padding: 20px; border-radius: 5px;">
            <div style="margin-bottom: 10px;">
                <label>Название на русском: *</label><br>
                <input type="text" id="newTitleRu" style="width: 100%; padding: 8px; margin-top: 5px;">
            </div>
            <div style="margin-bottom: 10px;">
                <label>Оригинальное название:</label><br>
                <input type="text" id="newTitle" style="width: 100%; padding: 8px; margin-top: 5px;">
            </div>
            <div style="margin-bottom: 10px;">
                <label>Год выпуска: *</label><br>
                <input type="number" id="newYear" min="1895" max="2025" value="2024" style="width: 100%; padding: 8px; margin-top: 5px;">
            </div>
            <div style="margin-bottom: 15px;">
                <label>Описание: *</label><br>
                <textarea id="newDescription" rows="4" style="width: 100%; padding: 8px; margin-top: 5px;"></textarea>
            </div>
            <button onclick="submitNewFilm()" style="padding: 10px 20px; background: #9C27B0; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Добавить фильм
            </button>
            <button onclick="fillFilmList()" style="padding: 10px 20px; background: #ccc; color: #333; border: none; border-radius: 4px; cursor: pointer; margin-left: 10px;">
                Отмена
            </button>
        </div>
    `;
}

// Функция добавления нового фильма
function submitNewFilm() {
    const title = document.getElementById('newTitle').value;
    const titleRu = document.getElementById('newTitleRu').value;
    const year = document.getElementById('newYear').value;
    const description = document.getElementById('newDescription').value;
    
    // Простая валидация
    if (!titleRu.trim()) {
        alert('Пожалуйста, введите название фильма на русском');
        return;
    }
    if (!year || year < 1895 || year > new Date().getFullYear()) {
        alert(`Пожалуйста, введите корректный год (1895-${new Date().getFullYear()})`);
        return;
    }
    if (!description.trim()) {
        alert('Пожалуйста, введите описание фильма');
        return;
    }
    
    const filmData = {
        title: title || titleRu, // Если оригинальное название пустое, используем русское
        title_ru: titleRu,
        year: parseInt(year),
        description: description
    };
    
    fetch('/lab7/rest-api/films/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filmData)
    })
    .then(function(response) {
        if (response.status === 201) {
            return response.json();
        } else {
            throw new Error('Ошибка добавления фильма');
        }
    })
    .then(function(result) {
        const output = document.getElementById('output');
        output.innerHTML = `<h3>Новый фильм успешно добавлен!</h3>
                           <p>ID нового фильма: <strong>${result.id}</strong></p>
                           <pre>${JSON.stringify(filmData, null, 2)}</pre>`;
        // Обновляем таблицу
        fillFilmList();
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при добавлении фильма');
    });
}

// Функция обновления статистики
function updateStats() {
    fetch('/lab7/rest-api/films/')
        .then(r => r.json())
        .then(films => {
            document.getElementById('films-count').textContent = films.length;
            document.getElementById('max-id').textContent = films.length > 0 ? films.length - 1 : 0;
        });
}

// Функция для отправки формы редактирования (добавим в глобальную область видимости)
window.editFilmSubmit = async function() {
    const id = document.getElementById('editId').value;
    const title = document.getElementById('editTitle').value;
    const titleRu = document.getElementById('editTitleRu').value;
    const year = document.getElementById('editYear').value;
    const description = document.getElementById('editDescription').value;
    
    // Валидация
    if (!titleRu.trim()) {
        alert('Пожалуйста, введите название фильма на русском');
        return;
    }
    if (!year || year < 1895 || year > new Date().getFullYear()) {
        alert(`Пожалуйста, введите корректный год (1895-${new Date().getFullYear()})`);
        return;
    }
    if (!description.trim()) {
        alert('Пожалуйста, введите описание фильма');
        return;
    }
    
    const filmData = {
        title: title,
        title_ru: titleRu,
        year: parseInt(year),
        description: description
    };
    
    try {
        const response = await fetch(`/lab7/rest-api/films/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filmData)
        });
        
        const output = document.getElementById('output');
        if (response.status === 200) {
            const updatedFilm = await response.json();
            output.innerHTML = `<h3>Фильм #${id} успешно обновлен!</h3><pre>${JSON.stringify(updatedFilm, null, 2)}</pre>`;
            // Обновляем таблицу
            fillFilmList();
        } else {
            const error = await response.json();
            output.innerHTML = `<h3>Ошибка редактирования:</h3><pre>${JSON.stringify(error, null, 2)}</pre>`;
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при обновлении фильма');
    }
};