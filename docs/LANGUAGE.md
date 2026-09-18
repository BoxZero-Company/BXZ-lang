# BXZ Language v1.2.2.1

```bxz
unit hello
  emit << "Hello from BXZ!"
seal
```

Variables:

```bxz
unit variables
  hold name := "Samyar"
  emit << name
seal
```

The `unit`, `hold`, `emit`, and `seal` surface is intentionally BXZ-specific.
