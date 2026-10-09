export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const CODE_KEY = "saarthi_access_code";

function readCode(): string {
  try {
    return window.localStorage.getItem(CODE_KEY) ?? "";
  } catch {
    return "";
  }
}

function saveCode(code: string): void {
  try {
    window.localStorage.setItem(CODE_KEY, code);
  } catch {
    /* storage unavailable: the code just won't be remembered */
  }
}

/**
 * fetch() against the Saarthi API. Sends the shared access code if one is stored and, on a 401,
 * asks the user for it once and retries.
 */
export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const send = () => {
    const code = readCode();
    const headers = { ...(init.headers as Record<string, string> | undefined) };
    if (code) headers["X-Access-Code"] = code;
    return fetch(`${API_URL}${path}`, { ...init, headers });
  };

  let res = await send();
  if (res.status === 401 && typeof window !== "undefined") {
    const entered = window.prompt("Enter the Saarthi access code");
    if (entered) {
      saveCode(entered.trim());
      res = await send();
    }
  }
  return res;
}
