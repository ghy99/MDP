# Commmunication Protocal

Communication Protocal used for the transmission of movement's intructions between STM, RPI, Algo and Andriod.

Each instruction is `5 char long`.

## Format

```c
/* [Key][motor direction][num_1][num_2][num_3] */

char aRxBuffer[5];

key = aRxBuffer[0];
motor_direction = aRxBuffer[1];
magnitude = ((int)(aRxBuffer[2])-48)*100 + ((int)(aRxBuffer[3])-48)*10 + ((int)(aRxBuffer[4])-48);

```

## Key

| Key |   Meaning   |
| --- | :---------: |
| S   |  Straight   |
| R   |    Right    |
| L   |    Left     |
| J   | Slide Right |
| K   | Slide Left  |

## Direction

| Dir | Meaning  |
| --- | :------: |
| F   | Forward  |
| B   | Backward |

## Magnitude

| Mag      | Meaning  |
| -------- | :------: |
| X X X    | Distance |
| \_ \_ \_ |  Angle   |

**Note**: It has to be 900, 090 or 009 format which equivalent to 900, 90 and 9 respectively.

## All Possible Combinations

| Instruction  |               Translation               |
| ------------ | :-------------------------------------: |
| S F X X X    |        Forward for XXX distance         |
| S B X X X    |        Backward for XXX distance        |
| R F \_ \_ \_ |    Right Forward for \_ \_ \_ Angle     |
| R B \_ \_ \_ |    Right Backward for \_ \_ \_ Angle    |
| L F \_ \_ \_ |     Left Forward for \_ \_ \_ Angle     |
| L B \_ \_ \_ |    Left Backward for \_ \_ \_ Angle     |
| J F \_ \_ \_ | Slide Right Forward for \_ \_ \_ Angle  |
| J B \_ \_ \_ | Slide Right Backward for \_ \_ \_ Angle |
| K F \_ \_ \_ |  Slide Left Forward for \_ \_ \_ Angle  |
| K B \_ \_ \_ | Slide Left Backward for \_ \_ \_ Angle  |
