import { writable, derived } from "svelte/store";

const storedToken = localStorage.getItem("token");
export const token = writable<string | null>(storedToken);

token.subscribe((value) => {
  if (value) {
    localStorage.setItem("token", value);
  } else {
    localStorage.removeItem("token");
  }
});

export const isAuthenticated = derived(token, ($token) => !!$token);

export function login(newToken: string) {
  token.set(newToken);
}

export function logout() {
  token.set(null);
}
