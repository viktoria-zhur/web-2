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
            output.innerHTML = `<h3>Редактирование фильма #${id}</h3>
                              <p>Заполните форму выше и нажмите "Обновить фильм"</p>`;
        })
        .catch(function(error) {
            console.error('Ошибка:', error);
            alert('Ошибка при загрузке данных фильма');
        });
}

// Функция удаления фильма
function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(function(response) {
        if (response.status === 204) {
            // Показываем сообщение
            const output = document.getElementById('output');
            output.innerHTML = `<h3>Фильм "${title}" успешно удален!</h3>`;
            
            // Перезагружаем таблицу после удаления
            setTimeout(fillFilmList, 500);
        } else {
            alert('Ошибка при удалении фильма');
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении фильма');
    });
}

// Функция для показа формы добавления
function addFilm() {
    // В будущем здесь будет показа формы добавления
    alert('Функция добавления фильма будет реализована в следующих пунктах');
}

// Функция обновления статистики
function updateStats() {
    fetch('/lab7/rest-api/films/')
        .then(r => r.json())
        .then(films => {
            document.getElementById('films-count').textContent = films.length;
            document.getElementById('max-id').textContent = films.length - 1;
        });
}