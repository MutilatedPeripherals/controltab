<script lang="ts">
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
  import { toast } from "svelte-sonner";

  import { useLogin } from "../../mutations/loginMutation";
  import { login } from "../../stores/auth";
  import { push } from "svelte-spa-router";

  let accessCode = $state("");

  const loginMutation = useLogin();

  const errorMessageDerived = $derived(
    () => $loginMutation.error?.message || ""
  );

  function handleLogin(event: Event) {
    event.preventDefault();
    $loginMutation.mutate(accessCode, {
      onSuccess: (token: string) => {
        login(token);
        push("/songs");
      },
    });
  }

  function handleRegister() {
    toast.info("Band registration is temporarily disabled", {
      description: "We are currently not accepting new band registrations. Please check back later.",
      duration: 4000
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
    <form onsubmit={handleLogin}>
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
        {#if errorMessageDerived()}
          <Alert variant="destructive">
            <AlertCircle class="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{errorMessageDerived()}</AlertDescription>
          </Alert>
        {/if}
      </CardContent>
      <CardFooter class="flex flex-col space-y-2">
        <Button type="submit" class="w-full mb-2">Access Dashboard</Button>
        <Button 
          type="button" 
          variant="outline" 
          class="w-full" 
          on:click={handleRegister}
        >
          Register New Band
        </Button>
      </CardFooter>
    </form>
  </Card>
</div>