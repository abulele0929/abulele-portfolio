const toggleBtn = document.getElementById('dark-toggle');
const html = document.documentElement;
const saved = localStorage.getItem('theme');

function setThemeLabel() {
  if (!toggleBtn) return;
  toggleBtn.textContent = html.classList.contains('dark') ? 'Light' : 'Dark';
}

if (saved === 'dark') html.classList.add('dark');
setThemeLabel();

if (toggleBtn) {
  toggleBtn.addEventListener('click', () => {
    html.classList.toggle('dark');
    localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    setThemeLabel();
  });
}

const currentPath = window.location.pathname.replace(/\/index\.html$/, '/') || '/';
document.querySelectorAll('[data-nav-path]').forEach((link) => {
  const navPath = link.getAttribute('data-nav-path');
  if (navPath === currentPath || (navPath === '/blog.html' && currentPath.endsWith('.html') && !currentPath.startsWith('/pages/'))) {
    link.classList.add('active');
    const glow = document.createElement('span');
    glow.className = 'tubelight-glow';
    link.appendChild(glow);
  }
});

const bar = document.getElementById('progress-bar');
if (bar) {
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? Math.min((scrollTop / docHeight) * 100, 100) : 0;
    bar.style.width = progress + '%';
  });
}

const scrollTopBtn = document.querySelector('.scroll-top-btn');
if (scrollTopBtn) {
  window.addEventListener('scroll', () => {
    scrollTopBtn.classList.toggle('visible', window.scrollY > 500);
  });
  scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}
