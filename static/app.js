async function fetchPassword() {
  const res = await fetch("/api/password", { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch password");
  const data = await res.json();
  return data.password;
}

function showToast(msg) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => (toast.textContent = ""), 1400);
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (_) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);
    return ok;
  }
}

async function refreshPassword() {
  const pwEl = document.getElementById("password");
  const btn = document.getElementById("refreshBtn");

  btn.disabled = true;
  btn.style.opacity = "0.7";

  try {
    const pw = await fetchPassword();
    pwEl.textContent = pw;
    showToast("New password generated");
  } catch (e) {
    showToast("Error generating password");
  } finally {
    btn.disabled = false;
    btn.style.opacity = "1";
  }
}

function wireUp() {
  const pwEl = document.getElementById("password");
  const btn = document.getElementById("refreshBtn");

  const doCopy = async () => {
    const text = pwEl.textContent.trim();
    const ok = await copyText(text);
    showToast(ok ? "Copied to clipboard" : "Copy failed");
  };

  pwEl.addEventListener("click", doCopy);
  pwEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      doCopy();
    }
  });

  btn.addEventListener("click", refreshPassword);
}

document.addEventListener("DOMContentLoaded", wireUp);
