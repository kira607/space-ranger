# SpaceRanger

A simple game in which you play as a pilot of a spaceship and fight other ships

```mermaid
---
title: Application structure
---
flowchart LR;
    id["Entrypoint('strat scene id')"]-->Application
    Application-->Scene1;
    Application-->Scene2;
    Scene1-->Object11;
    Scene1-->Object12;
    Scene2-->Object21;
    Scene2-->Object22;
    Object11-->Property111;
    Object11-->Property211;
    Object12-->Property112;
    Object12-->Property212;
    Object21-->Property121;
    Object21-->Property221;
    Object22-->Property122;
    Object22-->Property222;
```

# TODO

- [ ] Get rid off separate draw method call in game loop. Move draw logic in the rendering system.
