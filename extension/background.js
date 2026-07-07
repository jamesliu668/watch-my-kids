// 监听标签页更新（页面加载完成或 URL 改变）
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
    logActivity(tab.url, tab.title);
  }
});

// 监听标签页切换（用户点击了不同的标签）
chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.get(activeInfo.tabId, (tab) => {
    if (tab && tab.url && tab.url.startsWith('http')) {
      logActivity(tab.url, tab.title, true);
    }
  });
});

// 记录活动到本地存储
function logActivity(url, title, isActive = false) {
  chrome.storage.local.get(['logs'], (result) => {
    let logs = result.logs || [];
    
    // 避免重复记录完全相同的 URL
    const lastLog = logs[logs.length - 1];
    if (lastLog && lastLog.url === url) {
      return; 
    }

    const timestamp = new Date().toLocaleString();
    logs.push({
      time: timestamp,
      url: url,
      title: title || "No Title",
      active: isActive
    });

    // 限制存储数量，防止无限增长（保留最近 500 条）
    if (logs.length > 500) {
      logs = logs.slice(-500);
    }

    chrome.storage.local.set({ logs: logs });
  });
}

console.log("Watch My Kids: Monitor Active");
