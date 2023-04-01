# P1
## Cannot handle inputs where there is multiple of the same item
- repro
    ```
    > How many beef? 3
    ...
    > Jake got beef
    ...

    personal receipt attributes 3 orders of beef to each person that got beef
    ```

- initial solution: prompt user for number of items
    - "Jake got 1 beef"

# P2
## Flexible prompt formatting for all prompts
- confirmed "List of people" prompt does not handle
    ```
    # Expect
    Jake,Bobby,Katie
    # is the same as
    Jake, Bobby, Katie
    ```

## Verify counts of orders with counts of items
# P3
# P4
# P5