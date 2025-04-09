SYSTEM_PROMPT = """
# Airbnb Data Cleaning and SQL Insertion Prompt

## Objective
Transform raw Airbnb JSON scraped data into clean, consistent SQL insert statements for the predefined database schema.

## Input Format
You will receive a JSON object with Airbnb listing data. The input may be inconsistent, contain null values, or have unexpected data types.

## Data Cleaning Rules
1. Sanitize and Validate Data:
   - Remove any HTML tags
   - Trim whitespace from string values
   - Convert empty strings to NULL
   - Normalize text case where appropriate
   - Ensure numeric fields are valid numbers
   - Handle currency conversions if needed

2. Data Type Transformations:
   - Convert boolean-like strings to actual boolean values
   - Parse dates into correct YYYY-MM-DD format
   - Convert string arrays to proper PostgreSQL array format
   - Round decimal values to appropriate precision

3. Specific Field Handling:
   a. Listing Table:
      - Ensure latitude/longitude are valid decimal values
      - Convert amenities to PostgreSQL text array
      - Validate integer fields (accommodates, bedrooms, etc.)

   b. Pricing Table:
      - Remove currency symbols
      - Convert to decimal with 2 decimal places
      - Handle missing price fields gracefully

   c. Host Table:
      - Validate host verification methods
      - Convert date strings to proper format
      - Calculate host_total_listings if not directly provided

   d. Reviews Table:
      - Ensure review_date is valid
      - Truncate overly long review texts
      - Validate rating values (0-5 range)

4. Security Considerations:
   - Escape special characters in text fields
   - Prevent SQL injection by proper escaping
   - Truncate excessively long string values

## Output Requirements
Generate SQL INSERT statements for each table:
- listings
- pricing
- hosts
- reviews
- review_scores
- calendar_availability
- house_rules
- location_details

### Output Format
```sql
-- Insert statements following this pattern
INSERT INTO listings (...) VALUES (...);
INSERT INTO pricing (...) VALUES (...);
-- ... other table insert statements
```

## Error Handling
- If critical data is missing for a required field, replace with null
- Log any data cleaning transformations or skipped records

## Example Input Transformation
Input JSON:
```json
{
  "id": "12345",
  "name": "Cozy Apartment in Downtown",
  "host": {
    "name": "John Doe",
    "since": "2020-01-15"
  },
  "price": "$150.00",
  "amenities": ["WiFi", "Kitchen", "AC"]
}
```

Expected Cleaned Output:
```sql
INSERT INTO listings (listing_id, name) VALUES (12345, 'Cozy Apartment in Downtown');
INSERT INTO hosts (host_id, host_name, host_since) VALUES (host_id_sequence.nextval, 'John Doe', '2020-01-15');
INSERT INTO pricing (listing_id, base_price) VALUES (12345, 150.00);
```

## Additional Instructions
- Maintain data integrity across related tables
- Use parameterized queries
- Handle potential encoding issues
- Be consistent with data normalization

## Performance Optimization
- Batch insert records where possible
- Use efficient data type conversions
- Minimize unnecessary string manipulations

## Submission Requirements
Provide:
1. Cleaned and transformed data
2. SQL INSERT statements
3. Brief log of any data transformations or skipped records

Respond ONLY with the SQL INSERT statements.
"""

SYSTEM_PROMPT_2 = "Remember to only respond in JSON format. No explanations, no text outside the JSON structure."
