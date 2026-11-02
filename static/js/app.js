/* КнигоСайт — весь JS сайта */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Переводы для JS ---------- */
  const LANG = document.documentElement.lang || 'ru';
  const T = {
    ru: {
      confirmYes: 'Да, удалить', confirmNo: 'Отмена', toTop: 'Наверх',
      added: '✓ Добавлено', day: '☀️ День', sepia: '📜 Сепия', night: '🌙 Ночь',
      less: 'Меньше', more: 'Больше',
    },
    en: {
      confirmYes: 'Yes, delete', confirmNo: 'Cancel', toTop: 'Top',
      added: '✓ Added', day: '☀️ Day', sepia: '📜 Sepia', night: '🌙 Night',
      less: 'Smaller', more: 'Larger',
    },
    de: {
      confirmYes: 'Ja, löschen', confirmNo: 'Abbrechen', toTop: 'Nach oben',
      added: '✓ Hinzugefügt', day: '☀️ Tag', sepia: '📜 Sepia', night: '🌙 Nacht',
      less: 'Kleiner', more: 'Größer',
    },
  };
  const t = (T[LANG] || T.ru);

  /* ---------- Кнопка темы: иконка по текущей теме ---------- */
  const themeBtn = document.getElementById('theme-btn');
  if (themeBtn) {
    themeBtn.textContent =
      document.documentElement.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙';
  }

  /* ---------- Появление блоков при прокрутке ---------- */
  const revealTargets = document.querySelectorAll(
    '.book-card, .stat, .notification, .comment, .chapter-block, .profile-actions, .bookmark-list'
  );
  if ('IntersectionObserver' in window && revealTargets.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('reveal', 'in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach(el => { el.classList.add('reveal'); io.observe(el); });
  }

  /* ---------- Ctrl+K — фокус на поиск ---------- */
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      document.querySelector('.search-form input')?.focus();
    }
  });

  /* ---------- Мобильное меню ---------- */
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      nav.classList.toggle('open');
      burger.textContent = nav.classList.contains('open') ? '✕' : '☰';
    });
  }

  /* ---------- Сообщения (alert) скрываются сами ---------- */
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .4s, transform .4s';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-8px)';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  /* ---------- Подтверждение удаления ---------- */
  document.querySelectorAll('form[data-confirm]').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      showConfirm(form.dataset.confirm, () => form.submit());
    });
  });

  function showConfirm(text, onYes) {
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.innerHTML = `
      <div class="confirm-box">
        <p>${text}</p>
        <div class="confirm-actions">
          <button class="btn btn-danger" data-yes>${t.confirmYes}</button>
          <button class="btn" data-no style="background:#8b8378;box-shadow:none">${t.confirmNo}</button>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    overlay.querySelector('[data-yes]').onclick = () => { overlay.remove(); onYes(); };
    overlay.querySelector('[data-no]').onclick = () => overlay.remove();
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
  }

  /* ---------- Кнопка «наверх» ---------- */
  const toTop = document.createElement('button');
  toTop.className = 'to-top';
  toTop.title = t.toTop;
  toTop.textContent = '↑';
  document.body.appendChild(toTop);
  window.addEventListener('scroll', () => {
    toTop.classList.toggle('visible', window.scrollY > 400);
  });
  toTop.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });

  /* ---------- Читалка: размер шрифта, тема, стрелки ---------- */
  const readerText = document.querySelector('.reader-text');
  if (readerText) initReader();

  function initReader() {
    const root = document.documentElement;
    let size = parseFloat(localStorage.getItem('readerSize')) || 1.12;
    let theme = localStorage.getItem('readerTheme') || 'day';

    const apply = () => {
      root.style.setProperty('--reader-size', size + 'rem');
      document.body.classList.remove('reader-sepia', 'reader-night');
      if (theme !== 'day') document.body.classList.add('reader-' + theme);
      localStorage.setItem('readerSize', size);
      localStorage.setItem('readerTheme', theme);
      const label = document.getElementById('theme-label');
      if (label) label.textContent = { day: t.day, sepia: t.sepia, night: t.night }[theme];
    };

    const tools = document.createElement('div');
    tools.className = 'reader-tools';
    tools.innerHTML = `
      <button class="tool-btn" data-act="dec" title="${t.less}">А−</button>
      <button class="tool-btn" data-act="inc" title="${t.more}">А+</button>
      <button class="tool-btn" data-act="theme"><span id="theme-label"></span></button>`;
    const top = document.querySelector('.reader-top');
    if (top) top.appendChild(tools);

    tools.addEventListener('click', e => {
      const act = e.target.closest('[data-act]')?.dataset.act;
      if (act === 'inc') size = Math.min(size + 0.1, 1.8);
      if (act === 'dec') size = Math.max(size - 0.1, 0.9);
      if (act === 'theme') {
        theme = { day: 'sepia', sepia: 'night', night: 'day' }[theme];
      }
      apply();
    });
    apply();

    // стрелки ← → листают главы (первый — пред., последний — след.)
    document.addEventListener('keydown', e => {
      if (e.target.matches('input, textarea, select')) return;
      const links = document.querySelectorAll('.reader-nav a.btn');
      if (!links.length) return;
      if (e.key === 'ArrowLeft') links[0].click();
      if (e.key === 'ArrowRight') links[links.length - 1].click();
    });
  }

  /* ---------- Плеер: диск крутится пока играет ---------- */
  const audio = document.querySelector('.audio-player');
  const disc = document.querySelector('.player-disc');
  if (audio && disc) {
    audio.addEventListener('play', () => disc.classList.remove('paused'));
    audio.addEventListener('pause', () => disc.classList.add('paused'));
  }

  /* ---------- Закладки: мгновенная обратная связь ---------- */
  document.querySelectorAll('.bookmark-form').forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type=submit]');
      if (btn) {
        const old = btn.textContent;
        btn.textContent = t.added;
        btn.style.background = '#4a6741';
        setTimeout(() => { btn.textContent = old; btn.style.background = ''; }, 1500);
      }
    });
  });

  /* ---------- Рейтинг: подсветка звёзд при наведении ---------- */
  const starLabels = document.querySelectorAll('.star-rating label');
  starLabels.forEach(label => {
    label.addEventListener('mouseenter', () => {
      starLabels.forEach(l => l.style.transform = '');
      label.style.transform = 'scale(1.2)';
    });
  });

  /* ---------- Подсветка результатов поиска ---------- */
  const q = document.querySelector('.search-form input')?.value.trim();
  if (q && q.length > 1) {
    const re = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    document.querySelectorAll('.book-info h3, .book-detail-info h1').forEach(el => {
      if (re.test(el.innerHTML)) el.innerHTML = el.innerHTML.replace(re, '<mark class="search-highlight">$1</mark>');
    });
  }

});
