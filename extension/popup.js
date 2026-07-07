document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('log-container');
  const clearBtn = document.getElementById('clear-btn');

  // 读取存储的日志
  chrome.storage.local.get(['logs'], (result) => {
    const logs = result.logs || [];
    container.innerHTML = '';

    if (logs.length === 0) {
      container.innerHTML = '<p style="padding:10px; color:#888;">No logs found. Start browsing!</p>';
      return;
    }

    // 倒序显示，最新的在前面
    [...logs].reverse().forEach(log => {
      const div = document.createElement('div');
      div.className = `log-entry ${log.active ? 'active' : ''}`;
      div.innerHTML = `
        <div class="log-time">🕒 ${log.time} ${log.active ? '🔥 [Active]' : ''}</div>
        <div class="log-title">${log.title}</div>
        <div class="log-url">${log.url}</div>
      `;
      container.appendChild(div);
    });
  });

  // 清空日志功能
  clearBtn.addEventListener('click', () => {
    chrome.storage.local.set({ logs: [] }, () => {
      container.innerHTML = '<p style="padding:10px; color:#888;">History cleared.</p>';
    });
  });
});
