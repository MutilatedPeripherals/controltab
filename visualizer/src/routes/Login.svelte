<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { useLogin } from "../mutations/loginMutation";

  // State for access code and error messages
  let accessCode = "";
  let errorMessage = "";

  const loginMutation = useLogin();

  function handleLogin() {
    errorMessage = "";
    $loginMutation.mutate(accessCode, {
      onError: (error) => {
        errorMessage = error.message;
      },
    });
  }
</script>

<!-- Login form styled with DaisyUI and Tailwind -->
<div class="flex items-center justify-center min-h-screen bg-gray-100">
  <div class="p-8 bg-white shadow-lg rounded-lg w-96">
    <h2 class="text-2xl font-bold text-center mb-4">Band Login</h2>
    <form on:submit|preventDefault={handleLogin} class="space-y-4">
      <div class="form-control">
        <label class="label">
          <span class="label-text">Access Code</span>
        </label>
        <input
          type="text"
          placeholder="Enter your access code"
          bind:value={accessCode}
          class="input input-bordered w-full"
          required
        />
      </div>
      {#if errorMessage}
        <p class="text-red-500 text-sm">{errorMessage}</p>
      {/if}
      <button type="submit" class="btn btn-primary w-full">Login</button>
    </form>
  </div>
</div>
