<script>
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import {
    Alert,
    AlertDescription,
    AlertTitle,
  } from "$lib/components/ui/alert";
  import { AlertCircle, Music2 } from "lucide-svelte";

  import { useLogin } from "../mutations/loginMutation";
  import { login } from "../stores/auth";
  import { push } from "svelte-spa-router";

  let accessCode = "";
  let errorMessage = "";

  const loginMutation = useLogin();

  function handleLogin() {
    errorMessage = "";
    $loginMutation.mutate(accessCode, {
      onSuccess: (token) => {
        login(token);
        push("/songs");
      },
      onError: (error) => {
        errorMessage = error.message;
      },
    });
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-100">
  <Card class="w-full max-w-md">
    <CardHeader class="space-y-1">
      <div class="flex items-center justify-center mb-4">
        <Music2 class="h-12 w-12 text-primary" />
      </div>
      <CardTitle class="text-2xl font-bold text-center">Band Access</CardTitle>
      <CardDescription class="text-center">
        Enter your band's access code
      </CardDescription>
    </CardHeader>
    <form on:submit|preventDefault={handleLogin}>
      <CardContent class="space-y-4">
        <div class="space-y-2">
          <Label for="accessCode">Access Code</Label>
          <Input
            id="accessCode"
            type="password"
            placeholder="Enter your access code"
            bind:value={accessCode}
            required
          />
        </div>
        {#if errorMessage}
          <Alert variant="destructive">
            <AlertCircle class="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{errorMessage}</AlertDescription>
          </Alert>
        {/if}
      </CardContent>
      <CardFooter>
        <Button type="submit" class="w-full">Access Dashboard</Button>
      </CardFooter>
    </form>
  </Card>
</div>
